import tkinter as tk
from tkinter import messagebox
from tela_login import montar_tela_login
from  funcoes import verificar_login
from categoria import montar_tela_categoria
from veiculos import montar_tela_veiculos
from tela_ordens_servicos import montar_tela_os
import backup
import datetime

data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_backup = f"./backup/backup_banco_{data_atual}.db"

def montar_menu_principal():
    # Limpa a tela para voltar ao menu
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bem-vindo ao Sistema", font=("Arial", 16)).pack(pady=20)
    
    tk.Button(root, text="Abrir Cadastro de Veículos", 
              command=lambda: montar_tela_veiculos(root, montar_menu_principal), 
              width=30, height=2).pack(pady=10)
    
    tk.Button(root, text="Abrir Cadastro de Categorias",
              command=lambda: montar_tela_categoria(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)
    
    tk.Button(root, text="Abrir Ordens de Serviço",
              command=lambda: montar_tela_os(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)
    tk.Button(root, text="REALIZAR BACKUP", width=25, height=2, bg="#39A7FC", fg="white",
        command=lambda: backup.realizar_backup(
            'dados_frota.db',                                                               
            f"./backup/backup_banco_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db")).pack(pady=10)


def validar_login(usuario, senha):

    if verificar_login(usuario, senha):
        montar_menu_principal()

    else:
        messagebox.showerror(
            "Erro",
            "Usuário ou senha inválidos!"
        )

root = tk.Tk()
root.title("Sistema MecFrota")
root.state("zoomed")

# Inicia o sistema de login
montar_tela_login(root, validar_login)

# Inicia o sistema desenhando o menu
montar_menu_principal()

root.mainloop() 