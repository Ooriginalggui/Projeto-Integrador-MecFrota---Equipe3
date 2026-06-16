import tkinter as tk
from tkinter import messagebox
from tela_login import montar_tela_login

def montar_menu_principal():
    # Limpa a tela para voltar ao menu
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bem-vindo ao Sistema", font=("Arial", 16)).pack(pady=20)
    
    # Passamos a função 'montar_menu_principal' para as telas para que ela possa retornar ao menu após concluir suas operações
    tk.Button(root, text="Abrir Cadastro de Veículos", 
              command=lambda: montar_tela_veiculos(root, montar_menu_principal), 
              width=30, height=2).pack(pady=10)
    tk.Button(root, text="Abrir Cadastro de Categorias",
              command=lambda: montar_tela_categorias(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)
    tk.Button(root, text="Abrir Cadastro de Ordens de Serviço",
              command=lambda: montar_tela_ordens(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)

def validar_login(usuario, senha):

    if db_validar_login(usuario, senha):
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


root.mainloop()
