import tkinter as tk
from tkinter import messagebox, ttk
from tela_login import montar_tela_login
from funcoes import verificar_login
from categoria import montar_tela_categoria
from veiculos import montar_tela_veiculos
from tela_ordens_servicos import montar_tela_os
from modelos import montar_tela_modelos
import funcoes as bd
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
    
    tk.Button(root, text="Abrir Cadastro de Modelos",
              command=lambda: montar_tela_modelos(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)

    tk.Button(root, text="Abrir Cadastro de Categorias",
              command=lambda: montar_tela_categoria(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)
    
    tk.Button(root, text="Abrir Ordens de Serviço",
              command=lambda: montar_tela_os(root, montar_menu_principal),
              width=30, height=2).pack(pady=10)

    tk.Button(
        root, text="REALIZAR BACKUP", width=25, height=2, bg="#39A7FC", fg="white",
        command=lambda: backup.realizar_backup(
            'dados_frota.db',
            f"./backup/backup_banco_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
        )
    ).pack(pady=10)

    # --- TABELA DE VEÍCULOS COM REVISÃO ATRASADA ---
    tk.Label(
        root,
        text="VEÍCULOS COM A REVISÃO ATRASADA",
        font=("Arial", 12, "bold"),
        fg="red"
    ).pack(pady=(20, 5))

    frame_tabela = tk.Frame(root)
    frame_tabela.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    scrollbar_y = tk.Scrollbar(frame_tabela)
    scrollbar_y.pack(side="right", fill="y")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "modelo", "ano", "placa", "categoria", "data_saida", "data_proxima"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        height=8
    )
    scrollbar_y.config(command=tabela.yview)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)

    tabela.heading("id", text="ID", anchor="w")
    tabela.heading("modelo", text="Modelo", anchor="w")
    tabela.heading("ano", text="Ano", anchor="w")
    tabela.heading("placa", text="Placa", anchor="w")
    tabela.heading("categoria", text="Categoria", anchor="w")
    tabela.heading("data_saida", text="Data Saída", anchor="w")
    tabela.heading("data_proxima", text="Data Próxima Manutenção", anchor="w")

    tabela.column("id", width=50, anchor="w")
    tabela.column("modelo", width=220, anchor="w")
    tabela.column("ano", width=70, anchor="w")
    tabela.column("placa", width=110, anchor="w")
    tabela.column("categoria", width=160, anchor="w")
    tabela.column("data_saida", width=130, anchor="w")
    tabela.column("data_proxima", width=180, anchor="w")

    tabela.pack(fill="both", expand=True)

    # Tags de cor
    tabela.tag_configure("ate_1_mes", background="#fff59d")   # amarelo claro
    tabela.tag_configure("mais_1_mes", background="#ff9999")  # vermelho claro

    # Busca todos os veículos e filtra os atrasados
    hoje = datetime.datetime.now().date()
    um_mes_atras = hoje - datetime.timedelta(days=30)

    veiculos = bd.db_listar_veiculos()

    atrasados = 0

    for l in veiculos:
        if not l[6]:
            continue

        try:
            data_proxima_obj = datetime.datetime.strptime(l[6], "%Y-%m-%d").date()
        except:
            continue

        # Só entra se estiver atrasado (data_proxima < hoje)
        if data_proxima_obj >= hoje:
            continue

        # Formata datas para exibição
        data_saida_str = ""
        if l[5]:
            try:
                data_saida_str = datetime.datetime.strptime(l[5], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                data_saida_str = l[5]

        data_proxima_str = data_proxima_obj.strftime("%d/%m/%Y")

        # Define a cor: até 1 mês de atraso = amarelo, mais de 1 mês = vermelho
        if data_proxima_obj >= um_mes_atras:
            tag = "ate_1_mes"
        else:
            tag = "mais_1_mes"

        tabela.insert(
            "", "end",
            values=(l[0], l[1], l[2], l[3], l[4], data_saida_str, data_proxima_str),
            tags=(tag,)
        )
        atrasados += 1

    if atrasados == 0:
        # Mostra mensagem dentro da tabela se não houver atrasados
        tabela.insert("", "end", values=("", "Nenhum veículo com revisão atrasada", "", "", "", "", ""))

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