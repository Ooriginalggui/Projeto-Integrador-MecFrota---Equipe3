import tkinter as tk
from tkinter import messagebox, ttk
import funcoes as bd
import re
from datetime import datetime

def montar_tela_veiculos(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    # --- BOTÃO VOLTAR ---
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").pack(anchor="nw", padx=10, pady=5)

    # --- Título da Tela ---
    tk.Label(container, text="Cadastro de Veículos", font=("Arial", 14, "bold")).pack(pady=10)

    # --- Formulário de Cadastro ---

    # Busca categorias e modelos do banco
    categorias = bd.db_listar_categorias()
    map_categorias = {c[1]: c[0] for c in categorias}

    # Busca todos os modelos com categoria vinculada
    # db_listar_modelos retorna: (modelo_id, nome_modelo, nome_categoria)
    # Precisamos de (nome_modelo, categoria_id) para filtrar
    # Vamos buscar direto com buscar_modelos() que retorna (modelo_id, nome_modelo, categoria_id)
    todos_modelos = bd.buscar_modelos()
    # Monta dicionário: categoria_id -> lista de nomes de modelos
    modelos_por_categoria = {}
    for modelo in todos_modelos:
        cat_id = modelo[2]
        nome = modelo[1]
        if cat_id not in modelos_por_categoria:
            modelos_por_categoria[cat_id] = []
        modelos_por_categoria[cat_id].append(nome)

    # --- CATEGORIA (acima do modelo) ---
    tk.Label(container, text="Categoria:", font=("Arial", 10, "bold")).pack(pady=5)
    combo_categoria = ttk.Combobox(
        container,
        values=list(map_categorias.keys()),
        state="readonly",
        width=37
    )
    combo_categoria.pack()

    # --- MODELO (filtrado pela categoria selecionada) ---
    tk.Label(container, text="Modelo do Veículo:", font=("Arial", 10, "bold")).pack(pady=5)
    combo_modelo = ttk.Combobox(
        container,
        values=[],
        state="disabled",  # Começa desabilitado até selecionar categoria
        width=37
    )
    combo_modelo.pack()

    # Evento: quando categoria muda, filtra os modelos
    def ao_selecionar_categoria(event):
        categoria_nome = combo_categoria.get()
        if not categoria_nome:
            combo_modelo.set("")
            combo_modelo.config(values=[], state="disabled")
            return

        cat_id = map_categorias[categoria_nome]
        modelos_filtrados = modelos_por_categoria.get(cat_id, [])

        combo_modelo.set("")
        combo_modelo.config(
            values=modelos_filtrados,
            state="readonly" if modelos_filtrados else "disabled"
        )

        if not modelos_filtrados:
            messagebox.showinfo(
                "Aviso",
                f"Nenhum modelo cadastrado para a categoria '{categoria_nome}'."
            )

    combo_categoria.bind("<<ComboboxSelected>>", ao_selecionar_categoria)

    # --- ANO DO VEÍCULO ---
    tk.Label(container, text="Ano do Veículo:", font=("Arial", 10, "bold")).pack(pady=5)
    ent_ano = tk.Entry(container, width=40)
    ent_ano.pack()

    # --- PLACA DO VEÍCULO ---
    tk.Label(container, text="Placa do Veículo:", font=("Arial", 10, "bold")).pack(pady=5)
    ent_placa = tk.Entry(container, width=40)
    ent_placa.pack()

    # --- DATAS AUTOMÁTICAS ---
    hoje = datetime.now()
    mes = hoje.month + 6
    ano_prox = hoje.year
    if mes > 12:
        mes -= 12
        ano_prox += 1
    proxima = hoje.replace(year=ano_prox, month=mes)

    tk.Label(container, text="Data Saída (automática):", font=("Arial", 10, "bold")).pack(pady=5)
    lbl_data_saida = tk.Label(container, text=hoje.strftime("%d/%m/%Y"), font=("Arial", 10), relief="sunken", width=38)
    lbl_data_saida.pack()

    tk.Label(container, text="Data Próxima Manutenção (automática):", font=("Arial", 10, "bold")).pack(pady=5)
    lbl_data_proxima = tk.Label(container, text=proxima.strftime("%d/%m/%Y"), font=("Arial", 10), relief="sunken", width=38)
    lbl_data_proxima.pack()

    def salvar():
        modelo_veiculo = combo_modelo.get()
        ano_veiculo = ent_ano.get()
        placa_veiculo = ent_placa.get()
        categoria = combo_categoria.get()

        if modelo_veiculo and ano_veiculo and placa_veiculo and categoria:

            # Validação do ano
            try:
                ano = int(ano_veiculo)
                if ano < 1900 or ano > 2100:
                    messagebox.showwarning("Aviso", "O ano deve estar entre 1900 e 2100.")
                    return
            except ValueError:
                messagebox.showwarning("Aviso", "Digite um ano válido.")
                return

            # Validação da placa Mercosul
            placa_veiculo = placa_veiculo.upper()
            padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
            if not re.match(padrao_mercosul, placa_veiculo):
                messagebox.showwarning("Aviso", "Placa inválida. Exemplo: ABC1D23")
                return

            id_categoria = map_categorias[categoria]

            bd.db_cadastrar_veiculo(
                modelo_veiculo,
                ano_veiculo,
                placa_veiculo,
                id_categoria
            )

            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")

            combo_categoria.set("")
            combo_modelo.set("")
            combo_modelo.config(values=[], state="disabled")
            ent_ano.delete(0, tk.END)
            ent_placa.delete(0, tk.END)

            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    tk.Button(container, text="Cadastrar Veículo", command=salvar, bg="green", fg="white").pack(pady=10)

    # --- Lista de Veículos ---
    tk.Label(container, text="Veículos Cadastrados:", font=("Arial", 10, "bold")).pack(pady=10)

    frame_tabela = tk.Frame(container)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar_y = tk.Scrollbar(frame_tabela)
    scrollbar_y.pack(side="right", fill="y")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "modelo", "ano", "placa", "categoria", "data_saida", "data_proxima"),
        show="headings",
        yscrollcommand=scrollbar_y.set
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
    tabela.column("modelo", width=250, anchor="w")
    tabela.column("ano", width=80, anchor="w")
    tabela.column("placa", width=120, anchor="w")
    tabela.column("categoria", width=180, anchor="w")
    tabela.column("data_saida", width=150, anchor="w")
    tabela.column("data_proxima", width=180, anchor="w")

    tabela.pack(fill="both", expand=True)

    tabela.tag_configure("em_manutencao", background="yellow")
    tabela.tag_configure("atrasado", background="#ff9999")

    frame_botoes = tk.Frame(container)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes, text="Editar Selecionado",
        bg="green", fg="white",
        command=lambda: editar_selecionado()
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes, text="Excluir Selecionado",
        bg="red", fg="white",
        command=lambda: excluir_selecionado()
    ).pack(side="left", padx=10)

    def pegar_id_selecionado():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um veículo")
            return None
        valores = tabela.item(item[0], "values")
        return valores[0]

    def excluir_selecionado():
        id_veiculo = pegar_id_selecionado()
        if not id_veiculo:
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este veículo?"):
            bd.db_deletar_veiculo(id_veiculo)
            atualizar_lista()

    def editar_selecionado():
        id_veiculo = pegar_id_selecionado()
        if not id_veiculo:
            return
        editar(int(id_veiculo))

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        veiculos = bd.db_listar_veiculos()
        for l in veiculos:

            data_saida = ""
            if l[5]:
                try:
                    data_saida = datetime.strptime(l[5], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    data_saida = l[5]

            data_proxima_str = ""
            if l[6]:
                try:
                    data_proxima_str = datetime.strptime(l[6], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    data_proxima_str = l[6]

            tag = ""

            conn = bd.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM ordens_servicos
                WHERE veiculo_id = ?
                AND data_saida IS NULL
            """, (l[0],))
            em_manutencao = cursor.fetchone()[0]
            conn.close()

            if em_manutencao > 0:
                tag = "em_manutencao"
            else:
                try:
                    data_proxima_obj = datetime.strptime(l[6], "%Y-%m-%d")
                    if data_proxima_obj.date() < datetime.now().date():
                        tag = "atrasado"
                except:
                    pass

            tabela.insert(
                "", "end",
                values=(l[0], l[1], l[2], l[3], l[4], data_saida, data_proxima_str),
                tags=(tag,)
            )

    def editar(id_l):
        veiculos = bd.db_listar_veiculos()
        veiculo = next((l for l in veiculos if l[0] == id_l), None)

        if not veiculo:
            messagebox.showerror("Erro", "Veículo não encontrado")
            return

        janela = tk.Toplevel(container)
        janela.title("Editar Veículo")
        janela.geometry("400x480")

        categorias_edit = bd.db_listar_categorias()
        map_categorias_edit = {c[1]: c[0] for c in categorias_edit}

        todos_modelos_edit = bd.buscar_modelos()
        modelos_por_categoria_edit = {}
        for modelo in todos_modelos_edit:
            cat_id = modelo[2]
            nome = modelo[1]
            if cat_id not in modelos_por_categoria_edit:
                modelos_por_categoria_edit[cat_id] = []
            modelos_por_categoria_edit[cat_id].append(nome)

        # Categoria
        tk.Label(janela, text="Categoria").pack()
        combo_categoria_edit = ttk.Combobox(
            janela,
            values=list(map_categorias_edit.keys()),
            state="readonly",
            width=37
        )
        combo_categoria_edit.pack()
        combo_categoria_edit.set(veiculo[4])

        # Modelo (filtrado)
        tk.Label(janela, text="Modelo do Veículo").pack()
        cat_id_atual = map_categorias_edit.get(veiculo[4], None)
        modelos_iniciais = modelos_por_categoria_edit.get(cat_id_atual, [])
        combo_modelo_edit = ttk.Combobox(
            janela,
            values=modelos_iniciais,
            state="readonly",
            width=37
        )
        combo_modelo_edit.pack()
        combo_modelo_edit.set(veiculo[1])

        def ao_selecionar_categoria_edit(event):
            cat_nome = combo_categoria_edit.get()
            cat_id = map_categorias_edit.get(cat_nome)
            modelos_filtrados = modelos_por_categoria_edit.get(cat_id, [])
            combo_modelo_edit.set("")
            combo_modelo_edit.config(
                values=modelos_filtrados,
                state="readonly" if modelos_filtrados else "disabled"
            )

        combo_categoria_edit.bind("<<ComboboxSelected>>", ao_selecionar_categoria_edit)

        # Ano
        tk.Label(janela, text="Ano do Veículo").pack()
        ent_ano = tk.Entry(janela, width=40)
        ent_ano.pack()
        ent_ano.insert(0, veiculo[2])

        # Placa
        tk.Label(janela, text="Placa do Veículo").pack()
        ent_placa = tk.Entry(janela, width=40)
        ent_placa.pack()
        ent_placa.insert(0, veiculo[3])

        # Data Saída
        tk.Label(janela, text="Data Saída (dd/mm/aaaa)").pack()
        ent_data_saida = tk.Entry(janela, width=40)
        ent_data_saida.pack()
        ent_data_saida.insert(0, datetime.strptime(veiculo[5], "%Y-%m-%d").strftime("%d/%m/%Y"))

        # Data Próxima
        tk.Label(janela, text="Data Próxima (dd/mm/aaaa)").pack()
        ent_data_proxima = tk.Entry(janela, width=40)
        ent_data_proxima.pack()
        ent_data_proxima.insert(0, datetime.strptime(veiculo[6], "%Y-%m-%d").strftime("%d/%m/%Y"))

        def salvar_edicao():
            modelo_veiculo = combo_modelo_edit.get()
            ano_veiculo = ent_ano.get()
            placa_veiculo = ent_placa.get()
            categoria_nome = combo_categoria_edit.get()

            if not all([modelo_veiculo, ano_veiculo, placa_veiculo, categoria_nome]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            try:
                ano = int(ano_veiculo)
                if ano < 1900 or ano > 2100:
                    messagebox.showwarning("Aviso", "O ano deve estar entre 1900 e 2100.")
                    return
            except ValueError:
                messagebox.showwarning("Aviso", "Digite um ano válido.")
                return

            placa_veiculo = placa_veiculo.upper()
            padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
            if not re.match(padrao_mercosul, placa_veiculo):
                messagebox.showwarning("Aviso", "Placa inválida. Exemplo: ABC1D23")
                return

            id_categoria = map_categorias_edit[categoria_nome]
            data_saida = datetime.strptime(ent_data_saida.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_proxima = datetime.strptime(ent_data_proxima.get(), "%d/%m/%Y").strftime("%Y-%m-%d")

            bd.db_editar_veiculo(
                veiculo[0],
                modelo_veiculo,
                ano_veiculo,
                placa_veiculo,
                id_categoria,
                data_saida,
                data_proxima
            )

            atualizar_lista()
            messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
            janela.destroy()

        tk.Button(
            janela, text="Salvar Alterações",
            bg="green", fg="white",
            command=salvar_edicao
        ).pack(pady=20)

    atualizar_lista()