import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS experiencias')
cur.execute('DROP TABLE IF EXISTS cursos')


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
cur.execute(sql_profissionais)
cur.execute(sql_cursos)
cur.execute(sql_experiencias)

con.commit()
con.close()
