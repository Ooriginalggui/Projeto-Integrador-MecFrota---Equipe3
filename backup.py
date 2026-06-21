import sqlite3
from tkinter import messagebox



def realizar_backup (db_origem, db_destino ):
    conn_origem = None
    conn_destino = None


    try:
        conn_origem = sqlite3.connect(db_origem)
        conn_destino = sqlite3.connect(db_destino)


        with conn_destino:
            conn_origem.backup(conn_destino)

        messagebox.showinfo(
            "Backup",
            "Backup concluído com sucesso!"
        )
    except sqlite3.Error as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao realizar backup:\n{e}"
        )


    finally:
        if conn_origem:
            conn_origem.close()
        if conn_destino:
            conn_destino.close()