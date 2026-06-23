tabela_ordens_servicos = """
CREATE TABLE IF NOT EXISTS ordens_servicos (
    ordem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_entrada DATE,
    data_saida DATE,
    veiculo_id INTEGER,
    motivo VARCHAR(100),
    tipo_id INTEGER,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(veiculo_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_ordens(tipo_id)
);
"""

tabela_veiculos = """
CREATE TABLE IF NOT EXISTS veiculos (
    veiculo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa VARCHAR(100),
    modelo VARCHAR(100),
    ano VARCHAR(100),
    categoria_id INTEGER,
    data_saida VARCHAR(100),
    data_proxima VARCHAR(100),
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);
"""

tabela_usuarios = """
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_nome VARCHAR(100),
    senha VARCHAR(20)
);
"""

tabela_tipos_ordens = """
CREATE TABLE IF NOT EXISTS tipos_ordens (
    tipo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_tipo VARCHAR(100)
);
"""

tabela_categorias = """
CREATE TABLE IF NOT EXISTS categorias (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria VARCHAR(100)
);
"""
tabela_modelos = """
CREATE TABLE IF NOT EXISTS modelos (
    modelo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_modelo VARCHAR(100),
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);
"""