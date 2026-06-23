import sqlite3
import os
import script

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dados_frota.db")

def verificar_login(usuario, senha):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario_nome = ? AND senha = ?", (usuario, senha)
    )
    resultado = cursor.fetchone()
    print(f"Resultado: {resultado}")
    conn.close()
    return resultado is not None

def conectar():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(script.tabela_ordens_servicos)
    cursor.execute(script.tabela_usuarios)
    cursor.execute(script.tabela_veiculos)
    cursor.execute(script.tabela_categorias)
    cursor.execute(script.tabela_tipos_ordens)
    cursor.execute(script.tabela_modelos)
    conn.commit()
    return conn

def buscar_modelos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT modelo_id, nome_modelo, categoria_id FROM modelos")
    dados = cursor.fetchall()
    conn.close()
    return dados
 
lista_modelos = buscar_modelos()
 
nomes_modelos = [modelo[1] for modelo in lista_modelos]
categorias_modelos = {modelo[1]: modelo[2] for modelo in lista_modelos}
 

def db_cadastrar_modelo(nome_modelo, categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO modelos (nome_modelo, categoria_id) VALUES (?, ?)", (nome_modelo, categoria_id))
    conn.commit()
    conn.close()

def db_listar_modelos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT
                        m.modelo_id,
                        m.nome_modelo,
                        c.nome_categoria
                    FROM modelos m
                    JOIN categorias c
                        ON m.categoria_id = c.categoria_id
                    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_editar_modelos(nome_modelo, categoria_id, modelo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE modelos SET
                   nome_modelo = ?,
                   categoria_id = ?,
                   WHERE modelo_id = ?""", (nome_modelo, categoria_id, modelo_id))
    conn.commit()
    conn.close()

def db_deletar_modelo(modelo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM modelos WHERE modelo_id = ?", (modelo_id,))
    conn.commit()
    conn.close()


def db_cadastrar_veiculo(modelo, ano, placa, categoria_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO veiculos (
            modelo,
            ano,
            placa,
            categoria_id,
            data_saida,
            data_proxima
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            date('now'),
            date('now', '+6 months')
        )
    """, (modelo, ano, placa, categoria_id))

    conn.commit()
    conn.close()


def db_listar_veiculos():
    conn = conectar()
    cursor = conn.cursor()
    query = """
            SELECT
                v.veiculo_id,
                v.modelo,
                v.ano,
                v.placa,
                c.nome_categoria,
                v.data_saida,
                v.data_proxima
            FROM veiculos v
            INNER JOIN categorias c ON v.categoria_id = c.categoria_id
            ORDER BY v.veiculo_id
        """
       
    cursor.execute(query)
    veiculos = cursor.fetchall()
    conn.close()
    return    veiculos


def db_editar_veiculo(veiculo_id, modelo, ano, placa, categoria_id, data_saida, data_proxima):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE veiculos
        SET modelo = ?, ano = ?, placa = ?, categoria_id = ?, data_saida = ?, data_proxima = ?
        WHERE veiculo_id = ?
    """, (modelo, ano, placa, categoria_id, data_saida, data_proxima, veiculo_id))
    conn.commit()
    conn.close()


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
        WHERE categoria_id = ?
    """, (nome, id_categoria))
    conn.commit()
    conn.close()


def db_deletar_categorias(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE categoria_id = ?", (id_categoria,))
    conn.commit()
    conn.close()

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


def db_cadastrar_os(veiculo_id, motivo, tipo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ordens_servicos (
            data_entrada,
            data_saida,
            veiculo_id,
            motivo,
            tipo_id
        )
        VALUES (
            date('now'),
            NULL,
            ?,
            ?,
            ?
        )
    """, (veiculo_id, motivo, tipo_id))

    conn.commit()
    conn.close()

def db_listar_os():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            os.ordem_id,
            v.veiculo_id,
            v.modelo,
            t.nome_tipo,
            os.motivo,
            os.data_entrada,
            os.data_saida
        FROM ordens_servicos os
        INNER JOIN veiculos v
            ON os.veiculo_id = v.veiculo_id
        INNER JOIN tipos_ordens t
            ON os.tipo_id = t.tipo_id
        ORDER BY os.ordem_id DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

def db_concluir_os(ordem_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT data_saida FROM ordens_servicos WHERE ordem_id = ?
    """, (ordem_id,))

    resultado = cursor.fetchone()

    if resultado and resultado[0] is not None:
        conn.close()
        return False  # já foi concluída

    cursor.execute("""
        UPDATE ordens_servicos
        SET data_saida = date('now')
        WHERE ordem_id = ?
    """, (ordem_id,))

    cursor.execute("""
        SELECT veiculo_id, data_saida FROM ordens_servicos WHERE ordem_id = ?
    """, (ordem_id,))

    veiculo_id, data_saida = cursor.fetchone()

    cursor.execute("""
        UPDATE veiculos
        SET data_saida = ?, data_proxima = date(?, '+6 months')
        WHERE veiculo_id = ?
    """, (data_saida, data_saida, veiculo_id))

    conn.commit()
    conn.close()
    return True

def db_listar_tipos_os():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tipo_id,
            nome_tipo
        FROM tipos_ordens
        ORDER BY nome_tipo
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

def db_excluir_os(ordem_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM ordens_servicos
        WHERE ordem_id = ?
    """, (ordem_id,))

    conn.commit()
    conn.close()

def db_editar_os(
    ordem_id,
    veiculo_id,
    motivo,
    tipo_id
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ordens_servicos
        SET
            veiculo_id = ?,
            motivo = ?,
            tipo_id = ?
        WHERE ordem_id = ?
    """, (
        veiculo_id,
        motivo,
        tipo_id,
        ordem_id
    ))

    conn.commit()
    conn.close()

def db_verificar_manutencoes_pendentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.modelo, v.placa, v.data_proxima
        FROM veiculos v
        WHERE v.data_proxima IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 FROM ordens_servicos os
            WHERE os.veiculo_id = v.veiculo_id
            AND os.data_saida IS NULL
        )
        AND date(v.data_proxima) <= date('now')
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados