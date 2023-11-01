import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()


cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS experiencias')
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
    "num"       TEXT,
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

def cadastraProfissionais():
    cur.execute("INSERT INTO profissionais (nome, CPF, telefone, email, endereco, cidade, num, bairro, cep, uf ) values('Daniel', '703.968.604-00', '(87)9.81355794', 'danielverissimo1d@gmail.com', 'rua c', '08', 'centro', '55355000', 'paranatama-pe', 'pe')")
    con.commit()
    
def cadastraServicos():
    cur.execute("INSERT INTO servicos (nome, categoria, valor) values('formatação de PC', 'manutenção', 80 )")
    con.commit()

def cadastraCursos():
    cur.execute("INSERT INTO cursos (fk_idProfiss, modalidade, instituicao, area) VALUES(1, 'tecnico', 'ariano suassuna', 'informática')")
    con.commit()

def cadastraExperiencia():
    cur.execute("INSERT INTO experiencias (fk_IDprofiss, cargo, temp_servico, empresa) VALUES(1, 'atendente', '1a', 'j.i lanhouse')")
    con.commit()

cadastraProfissionais()
cadastraServicos()
cadastraCursos()
cadastraExperiencia()
con.close()

