import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS competencias')
cur.execute('DROP TABLE IF EXISTS cursos')


sql_profissional = '''CREATE TABLE "profissionais"(
    "ID_profiss" INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome"      TEXT,
    "sobrenome" TEXT,
    "CPF"       TEXT,
    "telefone"  TEXT,
    "email"     TEXT,
    "endereco"  TEXT,
    "num"       INTEGER,
    "bairro"    TEXT,
    "CEP"       TEXT,
    "uf"        TEXT,
    "complemento" TEXT
    )'''


sql_cursos = '''CREATE TABLE "competencias"(
    ID_compet INTEGER PRIMARY KEY AUTOINCREMENT,
)'''


sql_cursos = '''CREATE TABLE "cursos"(
    "fk_competencia"     INTEGER,
    "modalidade"    TEXT,
    "instituicao"   TEXT,
    "area"          TEXT,
    FOREIGN KEY ("fk_competencia") REFERENCES "competencias" ("ID_compet")
)'''


cur.execute(sql)
con.commit()
con.close()
