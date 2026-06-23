import tkinter as tk
from tkinter import messagebox, ttk
import funcoes as bd

def montar_tela_modelos(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").pack(anchor="nw", padx=10, pady=5)

    # --- Título da Tela ---
    tk.Label(container, text="Cadastro de Modelos dos Veículos", font=("Arial", 14, "bold")).pack(pady=10)
    # --- Formulário de Cadastro ---
    tk.Label(container, text="Nome do Modelo:", font=("Arial", 10, "bold")).pack(pady=5)
    ent_modelo = tk.Entry(container, width=40)
    ent_modelo.pack()


    # Combobox
    categorias = bd.db_listar_categorias()

    map_categorias = {c[1]: c[0] for c in categorias}

    # Categoria
    tk.Label(container, text="Categoria:", font=("Arial", 10, "bold")).pack(pady=5)

    combo_categoria = ttk.Combobox(
        container,
        values=list(map_categorias.keys()),
        state="readonly",
        width=37
    )

    combo_categoria.pack()


    def salvar():

        modelo = ent_modelo.get()

        nome_categoria = combo_categoria.get()

        if modelo and nome_categoria:

            id_categoria = map_categorias[nome_categoria]

            bd.db_cadastrar_modelo(
                modelo,
                id_categoria
            )

            messagebox.showinfo(
                "Sucesso",
                "Modelo cadastrado com sucesso!"
            )

            ent_modelo.delete(0, tk.END)

            combo_categoria.set("")

            atualizar_lista()

        else:
            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos!"
            )

    tk.Button(container, text="Cadastrar Modelo", command=salvar, bg="green", fg="white").pack(pady=10)

    # --- Lista de Modelos ---
    tk.Label(container, text="Modelos Cadastrados:", font=("Arial", 10, "bold")).pack(pady=10)
    
    # Frame da tabela
    frame_tabela = tk.Frame(container)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    # Scroll vertical
    scrollbar_y = tk.Scrollbar(frame_tabela)
    scrollbar_y.pack(side="right", fill="y")

    # Tabela
    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "modelo", "categoria"),
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
    tabela.heading("modelo", text="Modelo", anchor="w")
    tabela.heading("categoria", text="Categoria", anchor="w")

    # Larguras
    tabela.column("id", width=50, anchor="w")
    tabela.column("modelo", width=250, anchor="w")
    tabela.column("categoria", width=150, anchor="w")

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
                "Selecione um modelo"
            )
            return None

        valores = tabela.item(item[0], "values")

        return valores[0]

    def excluir_selecionado():
        id_modelo = pegar_id_selecionado()
        if not id_modelo:
            return
        if messagebox.askyesno(
            "Confirmar",
            "Deseja excluir este modelo?"
        ):
            bd.db_deletar_modelo(id_modelo)
            atualizar_lista()

    def editar_selecionado():
        id_modelo = pegar_id_selecionado()
        if not id_modelo:
            return
        editar(int(id_modelo))

    def atualizar_lista():

        # Limpa tabela
        for item in tabela.get_children():
            tabela.delete(item)

        modelos = bd.db_listar_modelos()

        for m in modelos:

            tabela.insert(
                "",
                "end",
                values=(
                    m[0],
                    m[1],
                    m[2],
                )
            )
    
    def editar(id_l):

        # Busca os dados atuais do livro
        modelos = bd.db_listar_modelos()

        modelo = None

        for m in modelos:
            if m[0] == id_l:
                modelo = m
                break

        if not modelo:
            messagebox.showerror("Erro", "Modelo não encontrado")
            return

        # Nova janela
        janela = tk.Toplevel(container)
        janela.title("Editar Modelo")
        janela.geometry("400x400")

        categorias = bd.db_listar_categorias()

        map_categorias = {c[1]: c[0] for c in categorias}

        # Nome
        tk.Label(janela, text="Nome do Modelo").pack()

        ent_nome = tk.Entry(janela, width=40)
        ent_nome.pack()
        ent_nome.insert(0, modelo[1])


        # Categoria
        tk.Label(janela, text="Categoria").pack()

        combo_categoria = ttk.Combobox(
            janela,
            values=list(map_categorias.keys()),
            state="readonly",
            width=37
        )

        combo_categoria.pack()
        combo_categoria.set(modelo[2])


        # Salvar
        def salvar_edicao():

            nome = ent_nome.get()
            id_categoria = map_categorias[combo_categoria.get()]

            bd.db_editar_modelo(
                nome,
                id_categoria,
                id_l
            )

            atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Modelo atualizado com sucesso!"
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