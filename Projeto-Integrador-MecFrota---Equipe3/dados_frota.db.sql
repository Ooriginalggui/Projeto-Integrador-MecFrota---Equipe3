BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categorias" (
	"categoria_id"	INTEGER,
	"nome_categoria"	VARCHAR(100),
	PRIMARY KEY("categoria_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ordens_servicos" (
	"ordem_id"	INTEGER,
	"data_entrada"	DATE,
	"data_saida"	DATE,
	"veiculo_id"	INTEGER,
	"motivo"	VARCHAR(100),
	"tipo_id"	INTEGER,
	PRIMARY KEY("ordem_id" AUTOINCREMENT),
	FOREIGN KEY("tipo_id") REFERENCES "tipos_ordens"("tipo_id"),
	FOREIGN KEY("veiculo_id") REFERENCES "veiculos"("veiculo_id")
);
CREATE TABLE IF NOT EXISTS "tipos_ordens" (
	"tipo_id"	INTEGER,
	"nome_tipo"	VARCHAR(100),
	PRIMARY KEY("tipo_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "usuarios" (
	"usuario_id"	INTEGER,
	"usuario_nome"	VARCHAR(100),
	"senha"	VARCHAR(100),
	PRIMARY KEY("usuario_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "veiculos" (
	"veiculo_id"	INTEGER,
	"placa"	VARCHAR(100),
	"modelo"	VARCHAR(100),
	"ano"	VARCHAR(100),
	"categoria_id"	INTEGER,
	"data_saida"	VARCHAR(100),
	"data_proxima"	VARCHAR(100),
	PRIMARY KEY("veiculo_id" AUTOINCREMENT),
	FOREIGN KEY("categoria_id") REFERENCES "categorias"("categoria_id")
);
INSERT INTO "categorias" VALUES (1,'Carro');
INSERT INTO "categorias" VALUES (2,'Moto');
INSERT INTO "ordens_servicos" VALUES (1,'2026-06-18','2026-06-18',1,'Preventiva',1);
INSERT INTO "ordens_servicos" VALUES (2,'2026-06-18','2026-06-19',1,'Troca de óleo',1);
INSERT INTO "ordens_servicos" VALUES (3,'2026-06-19',NULL,2,'Acidente de Trânsito',1);
INSERT INTO "ordens_servicos" VALUES (4,'2026-06-19',NULL,3,'Troca do pneu',2);
INSERT INTO "tipos_ordens" VALUES (1,'Preventiva');
INSERT INTO "tipos_ordens" VALUES (2,'Corretiva');
INSERT INTO "usuarios" VALUES (1,'ADMuser','admSENHA');
INSERT INTO "usuarios" VALUES (2,'ADMuser','admSENHA');
INSERT INTO "usuarios" VALUES (3,'user','senha');
INSERT INTO "usuarios" VALUES (4,'user','senha');
INSERT INTO "usuarios" VALUES (5,'admuser','admsenha');
INSERT INTO "usuarios" VALUES (6,'Pablo','Prof');
INSERT INTO "veiculos" VALUES (1,'ABC1A23','Bmw 330E','2021',1,'2026-06-19','2026-12-19');
INSERT INTO "veiculos" VALUES (2,'GOD1G67','Celta','2012',1,'2026-06-19','2026-12-19');
INSERT INTO "veiculos" VALUES (3,'FUN1G64','Biz','2009',2,'2026-06-19','2026-12-19');
COMMIT;
