import tkinter as tk
 
def montar_tela_login(root, verificar_login):
    # Limpa a janela caso haja algo nela
    for widget in root.winfo_children():
        widget.destroy()
 
    # Título centralizado na tela em negrito
    tk.Label(root, text="Login de Acesso", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Caixa de texto usuário
    tk.Label(root, text="Usuário:").pack()
    ent_usuario = tk.Entry(root)
    ent_usuario.pack(pady=5)

    # Caixa de texto senha
    tk.Label(root, text="Senha:").pack()
    ent_senha = tk.Entry(root)
    ent_senha.pack(pady=5)
 
    # Botão que executa a função de validação que virá do main.py
    btn = tk.Button(root, text="Entrar", command=lambda: verificar_login (ent_usuario.get(), ent_senha.get()))
    btn.pack(pady=20)