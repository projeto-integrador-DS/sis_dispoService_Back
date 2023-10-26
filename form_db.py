import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS experiencias')
cur.execute('DROP TABLE IF EXISTS cursos')
cur.execute('DROP TABLE IF EXISTS servicos')
cur.execute('DROP TABLE IF EXISTS oferece')


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
con.commit()

def cad_servicos():
    cur.execute("INSERT INTO servicos(nome, categoria, valor) values('formatação de computadores', 'manutencao', 40.00)")
    con.commit()
    con.row_factory=sql.Row
    cur.execute("SELECT * FROM servicos")
    servicos=cur.fetchall()
    con.close()
    print("os dados do servicos que vem do banco",servicos[0])

def alt_servicos():
    cur.execute("UPDATE servicos SET nome='instalação energia', categoria='construcao', valor=50 WHERE ID_servico=1")
    con.commit()
    con.close()
    return None

alt_servicos()
