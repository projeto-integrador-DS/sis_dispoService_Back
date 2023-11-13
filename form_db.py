import sqlite3 as sql

con = sql.connect('goservice.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS clientes')
cur.execute('DROP TABLE IF EXISTS profissionais')
cur.execute('DROP TABLE IF EXISTS experiencias')
cur.execute('DROP TABLE IF EXISTS experiencias')
cur.execute('DROP TABLE IF EXISTS cursos')
cur.execute('DROP TABLE IF EXISTS servicos')
cur.execute('DROP TABLE IF EXISTS oferece')


sql_clientes = '''CREATE TABLE "clientes"(
    "ID_clientes" INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome"      TEXT,
    "email"     TEXT,
    "cpf"       TEXT,
    "telefone"  TEXT,
    "rua"       TEXT,
    "numero"    TEXT,
    "bairro"    TEXT,
    "cidade"    TEXT,
    "estado"    TEXT,
    "cep"       TEXT
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

cur.execute(sql_clientes)
cur.execute(sql_profissionais)
cur.execute(sql_cursos)
cur.execute(sql_experiencias)
cur.execute(sql_servicos)
cur.execute(sql_oferece)
con.commit()

def cadastraClientes():
    cur.execute("INSERT INTO clientes (nome, cpf, telefone, email, rua, numero, cidade, bairro, cep, estado ) values('Marcelo', '088.617.184-93', '(87)9.81199151', 'devmarcelo.gus@gmail.com', 'rua João Gonçalves da SIlva', '115','Garanhuns', 'Boa Vista', '55292405', 'PE')")
    con.commit()

def cadastraProfissionais():
    cur.execute("INSERT INTO profissionais (ID_profiss, nome, CPF, telefone, email, endereco, cidade, num, bairro, cep, uf ) values(1, 'Daniel', '703.968.604-00', '(87)9.81355794', 'danielverissimo1d@gmail.com', 'rua c', '08', 'centro', '55355000', 'paranatama-pe', 'pe')")
    
    con.commit()
    
def cadastraServicos():
    cur.execute("INSERT INTO servicos (nome, categoria, valor) values('formatação de PC', 'manutenção', 80 )")
    con.commit()

def cadastraCursos():
    cur.execute("INSERT INTO cursos (fk_idProfiss, modalidade, instituicao, area) VALUES(1, 'tecnico', 'ariano suassuna', 'informática')")
    con.commit()

def cadastraExperiencia():
    cur.execute("INSERT INTO experiencias (fk_idprofiss, cargo, temp_servico, empresa) VALUES(1, 'pedreiro', '1a', 'j.i lanhouse')")
    con.commit()

cadastraClientes()
cadastraProfissionais()
cadastraServicos()
cadastraCursos()
cadastraExperiencia()
con.close()
