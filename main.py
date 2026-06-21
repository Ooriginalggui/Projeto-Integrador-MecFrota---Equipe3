import tkinter as tk
from tela_login import montar_tela_login
from funcoes import verificar_login
from categoria import montar_tela_categoria
from veiculos import montar_tela_veiculos
from tela_ordens_servicos import montar_tela_os
from funcoes import DB_PATH
import backup
import datetime
from tkinter import messagebox


def montar_menu_principal():
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
                  DB_PATH,
                  f"./backup/backup_banco_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
              )).pack(pady=10)

    verificar_alertas()


def verificar_alertas():
    from funcoes import db_verificar_manutencoes_pendentes
    hoje = datetime.datetime.today()
    pendentes = db_verificar_manutencoes_pendentes()

    atrasados = []
    hoje_lista = []

    for modelo, placa, data_proxima in pendentes:
        data = datetime.datetime.strptime(data_proxima, "%Y-%m-%d").date()
        if data < hoje:
            atrasados.append(f"  • {modelo} ({placa}) — venceu em {data.strftime('%d/%m/%Y')}")
        elif data == hoje:
            hoje_lista.append(f"  • {modelo} ({placa})")

    mensagem = ""

    if atrasados:
        mensagem += " Manutenção ATRASADA:\n" + "\n".join(atrasados)

    if hoje_lista:
        if mensagem:
            mensagem += "\n\n"
        mensagem += "Manutenção programada para HOJE:\n" + "\n".join(hoje_lista)

    if mensagem:
        messagebox.showwarning("Alertas de Manutenção", mensagem)

def validar_login(usuario, senha):
    if verificar_login(usuario, senha):
        montar_menu_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")


root = tk.Tk()
root.title("Sistema MecFrota")
root.state("zoomed")

montar_tela_login(root, validar_login)

root.mainloop()