import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS clientes')
cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS experiencias')
cur.execute('DROP TABLE IF EXISTS cursos')
cur.execute('DROP TABLE IF EXISTS servicos')
cur.execute('DROP TABLE IF EXISTS oferece')


sql_clientes = '''CREATE TABLE "clientes"(
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "EMAIL" TEXT,
    "CPF" TEXT,
    "TELEFONE" TEXT,
    "RUA" TEXT,
    "NUMERO" TEXT,
    "BAIRRO" TEXT,
    "CIDADE" TEXT,
    "ESTADO" TEXT,
    "CEP" TEXT,
    "FOTO" TEXT
    )'''

#cur.execute(sql)
'''con.commit()
con.close()
#con = sql.connect('goservice.db')
cur = con.cursor()'''



sql_profissionais = '''CREATE TABLE "profissionais"(
    "ID_profiss" INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome"      TEXT,
    "CPF"       TEXT,
    "telefone"  TEXT,
    "email"     TEXT,
    "endereco"  TEXT,
    "num"       INTEGER,
    "bairro"    TEXT,
    "CEP"       TEXT,
    cidade      TEXT,
    "uf"        TEXT
    )'''


sql_cursos = '''CREATE TABLE "cursos"(
    "ID_curso" INTEGER PRIMARY KEY AUTOINCREMENT,
    "fk_idProfiss"    INTEGER,
    "modalidade"    TEXT,
    "instituicao"   TEXT,
    "area"          TEXT,
    FOREIGN KEY ("fk_idProfiss") REFERENCES "profissionais" ("ID_profiss")
)'''


sql_experiencias='''CREATE TABLE "experiencias"(
    "ID_experiencia" INTEGER PRIMARY KEY AUTOINCREMENT,
    "fk_IDprofiss"    INTEGER,
    "cargo"         TEXT,
    "temp_servico"  TEXT,
    "empresa"       TEXT,
    FOREIGN KEY ("fk_IDprofiss") REFERENCES "profissionais" ("ID_profiss")
)
'''
sql_servicos='''CREATE TABLE "servicos" (
    "ID_servico"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome"          TEXT,
    "categoria"     TEXT,
    "valor"         REAL
)
'''
sql_oferece='''CREATE TABLE "oferece"(
    "fk_profiss" INTEGER,
    "fk_servic"  INTEGER,
    FOREIGN KEY ("fk_profiss") REFERENCES "profissionais" ("ID_profiss"),
    FOREIGN KEY ("fk_servic") REFERENCES "servicos" ("ID_servico")
)'''

cur.execute(sql_profissionais)
cur.execute(sql_cursos)
cur.execute(sql_experiencias)
cur.execute(sql_servicos)
cur.execute(sql_oferece)
cur.execute(sql_clientes)
con.commit()
