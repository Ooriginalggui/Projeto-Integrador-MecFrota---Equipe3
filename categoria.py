import tkinter as tk
from tkinter import messagebox, ttk
import funcoes as bd

def montar_tela_categoria(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()


    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").pack(anchor="nw", padx=10, pady=5)


    tk.Label(container, text="Cadastro de Categorias", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(container, text="Nome da Categoria:", font=("Arial", 10, "bold")).pack(pady=5)
    ent_nome = tk.Entry(container, width=40)
    ent_nome.pack()

    def salvar():

        nome_categoria = ent_nome.get()

        if nome_categoria:

            bd.db_cadastrar_categorias(
                nome_categoria
            )

            messagebox.showinfo(
                "Sucesso",
                "Categoria cadastrada com sucesso!"
            )

            ent_nome.delete(0, tk.END)

            atualizar_lista()

        else:
            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos!"
            )

    tk.Button(container, text="Cadastrar Categoria", command=salvar, bg="green", fg="white").pack(pady=10)

    # --- Lista de Categorias ---
    tk.Label(container, text="Categorias Cadastradas:", font=("Arial", 10, "bold")).pack(pady=10)
    
    # Frame da tabela
    frame_tabela = tk.Frame(container)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    # Scroll vertical
    scrollbar_y = tk.Scrollbar(frame_tabela)
    scrollbar_y.pack(side="right", fill="y")

    # Tabela
    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "nome"),
        show="headings",
        yscrollcommand=scrollbar_y.set
    )

    scrollbar_y.config(command=tabela.yview)

    # Estilo
    style = ttk.Style()

    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold")
    )

    style.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=25
    )

    # Cabeçalhos
    tabela.heading("id", text="ID", anchor="w")
    tabela.heading("nome", text="Nome", anchor="w")

    # Colunas
    tabela.column("id", width=80, anchor="w")
    tabela.column("nome", width=400, anchor="w")

    # Larguras
    tabela.column("id", width=50)
    tabela.column("nome", width=250)

    tabela.pack(fill="both", expand=True)

    frame_botoes = tk.Frame(container)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Editar Selecionado",
        bg="green",
        fg="white",
        command=lambda: editar_selecionado()
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="Excluir Selecionado",
        bg="red",
        fg="white",
        command=lambda: excluir_selecionado()
    ).pack(side="left", padx=10)

    def pegar_id_selecionado():
        item = tabela.selection()

        if not item:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma categoria"
            )
            return None

        valores = tabela.item(item[0], "values")

        return valores[0]

    def excluir_selecionado():
        id_categoria = pegar_id_selecionado()
        if not id_categoria:
            return
        if messagebox.askyesno(
            "Confirmar",
            "Deseja excluir esta categoria?"
        ):
            bd.db_deletar_categorias(id_categoria)
            atualizar_lista()

    def editar_selecionado():
        id_categoria = pegar_id_selecionado()
        if not id_categoria:
            return
        editar(int(id_categoria))

    def atualizar_lista():

        # Limpa tabela
        for item in tabela.get_children():
            tabela.delete(item)

        categorias = bd.db_listar_categorias()

        for l in categorias:

            tabela.insert(
                "",
                "end",
                values=(
                    l[0],
                    l[1],
                )
            )
    
    def editar(id_l):

        # Busca os dados atuais do livro
        categorias = bd.db_listar_categorias()

        categoria = None

        for l in categorias:
            if l[0] == id_l:
                categoria = l
                break

        if not categoria:
            messagebox.showerror("Erro", "Categoria não encontrada")
            return

        # Nova janela
        janela = tk.Toplevel(container)
        janela.title("Editar Categoria")
        janela.geometry("400x400")

        # Nome
        tk.Label(janela, text="Nome da Categoria").pack()

        ent_nome = tk.Entry(janela, width=40)
        ent_nome.pack()
        ent_nome.insert(0, categoria[1])

        # Salvar
        def salvar_edicao():

            nome_categoria = ent_nome.get()

            bd.db_atualizar_categorias(
                id_l,
                nome_categoria
            )

            atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Categoria atualizada com sucesso!"
            )

            janela.destroy()

        tk.Button(
            janela,
            text="Salvar Alterações",
            bg="green",
            fg="white",
            command=salvar_edicao
        ).pack(pady=20)

    atualizar_lista()