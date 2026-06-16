import sqlite3
import os
import script

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dados_frota.db")

def verificar_login(usuario, senha):
    conectar().close()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login WHERE usuario = ? AND senha = ?", (usuario, senha)
    )
    resultado = cursor.fetchone()


    conn.close()


    if resultado:
        return True
    else:
        return False


def conectar():
    conn = sqlite3.connect(DB_PATH) # Alterado para usar DB_PATH e manter o padrão do seu arquivo
    cursor = conn.cursor()
    cursor.execute(script.tabela_ordens_servicos)
    cursor.execute(script.tabela_usuarios)
    cursor.execute(script.tabela_veiculos)
    cursor.execute(script.tabela_categorias)
    cursor.execute(script.tabela_tipos_ordens)
    conn.commit()
    return conn


def db_cadastrar_veiculo(placa, modelo, ano, categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    # Adicionado o campo 'status' obrigatoriamente como 'Disponivel' de acordo com a nova tabela
    cursor.execute("""
        INSERT INTO veiculos (placa, modelo, ano, categoria_id)
        VALUES (?, ?, ?, ?)
    """, (placa, modelo, ano, categoria_id))
    conn.commit()
    conn.close()


def db_listar_veiculos():
    conn = conectar()
    cursor = conn.cursor()
    query = """
            SELECT
                v.veiculo_id,
                v.placa,
                v.modelo,
                v.ano,
                c.nome_categoria
            FROM veiculos v
            INNER JOIN categorias c ON v.categoria_id = c.categoria_id
            ORDER BY v.veiculo_id
        """
       
    cursor.execute(query)
    veiculos = cursor.fetchall()
    conn.close()
    return    veiculos


def db_atualizar_veiculo(id_veiculo, placa, modelo, ano, categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE veiculos
        SET placa = ?, modelo = ?, ano = ?, categoria_id = ?
        WHERE veiculo_id = ?
    """, (placa, modelo, ano, categoria_id, id_veiculo))
    conn.commit()
    conn.close()


def db_deletar_veiculo(id_veiculo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM veiculos WHERE veiculo_id = ?", (id_veiculo,))
    conn.commit()
    conn.close()

# def db_cadastrar_cliente(nome_cliente, telefone, endereco, cpf, tipo):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO cliente (nome_cliente, telefone, endereco, cpf, tipo)
#         VALUES (?, ?, ?, ?, ?)
#     """, (nome_cliente, telefone, endereco, cpf, tipo))
#     conn.commit()
#     conn.close()

# def db_atualizar_cliente(id_cliente, nome, telefone, endereco, cpf, tipo):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("""
#         UPDATE cliente
#         SET nome_cliente = ?, telefone = ?, endereco = ?, cpf = ?, tipo = ?
#         WHERE id_cliente = ?
#     """, (nome, telefone, endereco, cpf, id_cliente, tipo))
#     conn.commit()
#     conn.close()


# def db_listar_cliente():
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM cliente")
#     dados = cursor.fetchall()
#     conn.close()
#     return dados


# def db_deletar_cliente(id_cliente):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
#     conn.commit()
#     conn.close()


def db_cadastrar_categorias(nome_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nome_categoria) VALUES (?)", (nome_categoria,))
    conn.commit()
    conn.close()


def db_listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    dados = cursor.fetchall()
    conn.close()
    return dados


def db_atualizar_categorias(id_categoria, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categorias
        SET nome_categoria = ?
        WHERE id_categoria = ?
    """, (nome, id_categoria))
    conn.commit()
    conn.close()


def db_deletar_categorias(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))
    conn.commit()
    conn.close()


# def db_cadastrar_categoria(nome_cat):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO categoria (nome_categoria) VALUES (?)", (nome_cat,))
#     conn.commit()
#     conn.close()


# def db_listar_categoria():
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM categoria")
#     dados = cursor.fetchall()
#     conn.close()
#     return dados


# def db_atualizar_categoria(id_categoria, nome):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("""
#         UPDATE categoria
#         SET nome_categoria = ?
#         WHERE id_categoria = ?
#     """, (nome, id_categoria))
#     conn.commit()
#     conn.close()


# def db_deletar_categoria(id_categoria):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM categoria WHERE id_categoria = ?", (id_categoria,))
#     conn.commit()
#     conn.close()


# def db_cadastrar_autor(nome_autor):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO autor (nome_autor) VALUES (?)", (nome_autor,))
#     conn.commit()
#     conn.close()
   
# def db_atualizar_autor(id_autor, nome):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("""
#         UPDATE autor
#         SET nome_autor = ?
#         WHERE id_autor = ?
#     """, (nome, id_autor))
#     conn.commit()
#     conn.close()


# def db_listar_autor():
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM autor")
#     dados = cursor.fetchall()
#     conn.close()
#     return dados


# def db_deletar_autor(id_autor):
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM autor WHERE id_autor = ?", (id_autor,))
#     conn.commit()
#     conn.close()


def db_cadastrar_manutencao(veiculo_id, motivo, tipo_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ordens_servicos (data_ultima, data_proxima, veiculo_id, motivo, tipo_id)
            VALUES (datetime('now'), datetime('now', '+180 days'), ?, ?, ?)
        """, (veiculo_id, motivo, tipo_id))

        cursor.execute("""
            UPDATE veiculos SET status = 'Na Oficina' WHERE veiculo_id = ?
        """, (veiculo_id,))

        conn.commit()
    except Exception as e:
        print(f"Erro ao cadastrar manutenção: {e}")
    finally:
        conn.close()


def db_listar_manutencao():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                os.ordem_id,
                v.modelo,
                v.status,
                t.nome_tipo,
                os.motivo,
                os.data_ultima,
                os.data_proxima
            FROM ordens_servicos os
            JOIN veiculos v ON v.veiculo_id = os.veiculo_id
            JOIN tipos_ordens t ON t.tipo_id = os.tipo_id
            ORDER BY os.data_ultima DESC
        """)
        dados = cursor.fetchall()
        return dados
    except Exception as e:
        print(f"Erro ao listar manutenções: {e}")
        return []
    finally:
        conn.close()


def db_concluir_manutencao(veiculo_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE veiculos SET status = 'Disponivel para uso' WHERE veiculo_id = ?
        """, (veiculo_id,))

        conn.commit()
    except Exception as e:
        print(f"Erro ao concluir manutenção: {e}")
    finally:
        conn.close()