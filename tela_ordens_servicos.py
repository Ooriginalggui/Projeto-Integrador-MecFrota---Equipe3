import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import funcoes as bd


def montar_tela_os(container, funcao_voltar):

    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(
        container,
        text="← Voltar ao Menu",
        command=funcao_voltar,
        bg="#ccc"
    ).pack(anchor="nw", padx=10, pady=5)

    tk.Label(
        container,
        text="Cadastro de Ordens de Serviço",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    veiculos = bd.db_listar_veiculos()
    mapa_veiculos = {
        f"{v[0]} - {v[1]}": v[0]
        for v in veiculos
    }

    tipos = bd.db_listar_tipos_os()
    mapa_tipos = {
        t[1]: t[0]
        for t in tipos
    }

    tk.Label(
        container,
        text="Veículo:",
        font=("Arial", 10, "bold")
    ).pack()

    combo_veiculo = ttk.Combobox(
        container,
        values=list(mapa_veiculos.keys()),
        width=40,
        state="readonly"
    )
    combo_veiculo.pack(pady=5)

    tk.Label(
        container,
        text="Tipo de Manutenção:",
        font=("Arial", 10, "bold")
    ).pack()

    combo_tipo = ttk.Combobox(
        container,
        values=list(mapa_tipos.keys()),
        width=40,
        state="readonly"
    )
    combo_tipo.pack(pady=5)

    tk.Label(
        container,
        text="Motivo:",
        font=("Arial", 10, "bold")
    ).pack()

    ent_motivo = tk.Entry(
        container,
        width=50
    )
    ent_motivo.pack(pady=5)

    hoje = datetime.now().strftime("%d/%m/%Y")

    tk.Label(
        container,
        text="Data Entrada (automática):",
        font=("Arial", 10, "bold")
    ).pack()

    lbl_data = tk.Label(
        container,
        text=hoje,
        relief="sunken",
        width=30
    )
    lbl_data.pack(pady=5)

    # ID da OS em edição (None = modo cadastro)
    id_editando = [None]

    def limpar_campos():
        combo_veiculo.set("")
        combo_tipo.set("")
        ent_motivo.delete(0, tk.END)
        id_editando[0] = None
        btn_salvar.config(text="Cadastrar OS", bg="green")
        lbl_data.config(text=hoje)

    def preencher_para_editar(os):
        limpar_campos()
        id_editando[0] = os[0]
        chave_veiculo = next((k for k in mapa_veiculos if os[1] in k), "")
        combo_veiculo.set(chave_veiculo)
        ent_motivo.delete(0, tk.END)
        ent_motivo.insert(0, os[3])
        btn_salvar.config(text="Atualizar OS", bg="orange")
        lbl_data.config(text=os[4])

    def salvar():
        veiculo = combo_veiculo.get()
        tipo = combo_tipo.get()
        motivo = ent_motivo.get()

        if not veiculo or not tipo or not motivo:
            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos."
            )
            return

        if id_editando[0] is None:
            bd.db_cadastrar_os(
                mapa_veiculos[veiculo],
                motivo,
                mapa_tipos[tipo]
            )
            messagebox.showinfo("Sucesso", "OS cadastrada.")
        else:
            bd.db_editar_os(
                id_editando[0],
                mapa_veiculos[veiculo],
                motivo,
                mapa_tipos[tipo]
            )
            messagebox.showinfo("Sucesso", "OS atualizada.")
        
        limpar_campos()
        atualizar_lista()

    btn_salvar = tk.Button(
        container,
        text="Cadastrar OS",
        command=salvar,
        bg="green",
        fg="white"
    )
    btn_salvar.pack(pady=10)

    tk.Label(
        container,
        text="Ordens de Serviço:",
        font=("Arial", 10, "bold")
    ).pack(pady=10)

    frame_tabela = tk.Frame(container)
    frame_tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=(
            "id",
            "veiculo",
            "tipo",
            "motivo",
            "entrada",
            "saida"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("veiculo", text="Veículo")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("motivo", text="Motivo")
    tabela.heading("entrada", text="Data Entrada")
    tabela.heading("saida", text="Data Saída")

    tabela.column("id", width=50)
    tabela.column("veiculo", width=250)
    tabela.column("tipo", width=150)
    tabela.column("motivo", width=300)
    tabela.column("entrada", width=120)
    tabela.column("saida", width=120)

    tabela.pack(
        fill="both",
        expand=True
    )

    tabela.tag_configure(
        "em_manutencao",
        background="yellow"
    )

    def atualizar_lista():

        for item in tabela.get_children():
            tabela.delete(item)

        dados = bd.db_listar_os()

        for os in dados:

            entrada = datetime.strptime(
                os[5],
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            saida = ""

            if os[6]:
                saida = datetime.strptime(
                    os[6],
                    "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

            tag = ""

            if not os[6]:
                tag = "em_manutencao"

            tabela.insert(
                "",
                "end",
                values=(
                    os[0],
                    os[2],
                    os[3],
                    os[4],
                    entrada,
                    saida
                ),
                tags=(tag,)
            )

    def pegar_id():

        item = tabela.selection()

        if not item:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma OS."
            )
            return None

        return tabela.item(item[0], "values")[0]

    def concluir():
        ordem_id = pegar_id()
        if not ordem_id:
            return

        sucesso = bd.db_concluir_os(ordem_id)

        if sucesso:
            atualizar_lista()
            messagebox.showinfo("Sucesso", "Veículo retornou da manutenção.")
        else:
            messagebox.showwarning("Aviso", "Esta OS já foi concluída e não pode ser alterada novamente.")

    def excluir_os():

        ordem_id = pegar_id()

        if not ordem_id:
            return

        if messagebox.askyesno(
            "Confirmar",
            "Deseja excluir esta OS?"
        ):
            bd.db_excluir_os(ordem_id)
            atualizar_lista()

    def editar_os():

        item = tabela.selection()

        if not item:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma OS."
            )
            return

        valores = tabela.item(item[0], "values")
       
        preencher_para_editar(valores)

    frame_botoes = tk.Frame(container)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Editar Selecionado",
        bg="green",
        fg="white",
        command=editar_os
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="Excluir Selecionado",
        bg="red",
        fg="white",
        command=excluir_os
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="Veículo Retornou",
        bg="blue",
        fg="white",
        command=concluir
    ).pack(side="left", padx=10)

    atualizar_lista()