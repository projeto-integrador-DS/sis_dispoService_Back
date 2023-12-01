from werkzeug.security import generate_password_hash
import sqlite3 as sql
def setup():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    con = sql.connect('goservice.db', detect_types=sql.PARSE_DECLTYPES)
    con.execute('PRAGMA foreign_keys = ON')

    sql_clientes = '''CREATE TABLE IF NOT EXISTS "clientes"(
        "ID_clientes" INTEGER PRIMARY KEY AUTOINCREMENT,
        "nome" TEXT,
        "email" TEXT,
        "cpf" TEXT,
        "telefone" TEXT,
        "rua" TEXT,
        "numero" TEXT,
        "bairro" TEXT,
        "cidade" TEXT,
        "estado" TEXT,
        "cep" TEXT
        )'''

    sql_profissionais = '''CREATE TABLE IF NOT EXISTS "profissionais"(
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
        "uf"        TEXT,
        "profissao" TEXT
        )'''
    


    sql_cursos = '''CREATE TABLE IF NOT EXISTS "cursos"(
        "ID_curso" INTEGER PRIMARY KEY AUTOINCREMENT,
        "fk_idProfiss"    INTEGER,
        "modalidade"    TEXT,
        "instituicao"   TEXT,
        "area"          TEXT,
        FOREIGN KEY ("fk_idProfiss") REFERENCES "profissionais" ("ID_profiss") ON DELETE CASCADE
    )'''


    sql_experiencias='''CREATE TABLE IF NOT EXISTS "experiencias"(
        "ID_experiencia" INTEGER PRIMARY KEY AUTOINCREMENT,
        "fk_IDprofiss"    INTEGER,
        "cargo"         TEXT,
        "temp_servico"  TEXT,
        "empresa"       TEXT,
        FOREIGN KEY ("fk_IDprofiss") REFERENCES "profissionais" ("ID_profiss") ON DELETE CASCADE
    )
    '''
    sql_servicos='''CREATE TABLE IF NOT EXISTS "servicos" (
        "ID_servico"    INTEGER PRIMARY KEY AUTOINCREMENT,
        "nome"          TEXT,
        "categoria"     TEXT,
        "valor"         REAL
    )
    '''
    sql_oferece='''CREATE TABLE IF NOT EXISTS "oferece"(
        "fk_profiss" INTEGER,
        "fk_servic"  INTEGER,
        FOREIGN KEY ("fk_profiss") REFERENCES "profissionais" ("ID_profiss") ON DELETE CASCADE,
        FOREIGN KEY ("fk_servic") REFERENCES "servicos" ("ID_servico") ON DELETE CASCADE
    )'''

    sql_login='''CREATE TABLE IF NOT EXISTS "loginProf"(
        "fk_profiss" INTEGER,
        "username"  TEXT,
        "senha"     TEXT,
        FOREIGN KEY ("fk_profiss") REFERENCES "profissionais" ("ID_profiss") ON DELETE CASCADE
    )
    '''
    sql_login_cli = '''CREATE TABLE IF NOT EXISTS "loginCli"(
    "fk_cli" INTEGER,
    "username"  TEXT,
    "senha"     TEXT,
    FOREIGN KEY ("fk_cli") REFERENCES "clientes" ("ID_clientes") ON DELETE CASCADE
)
'''

    cur.execute(sql_login)
    cur.execute(sql_clientes)
    cur.execute(sql_login_cli)
    cur.execute(sql_profissionais)
    cur.execute(sql_cursos)
    cur.execute(sql_experiencias)
    cur.execute(sql_servicos)
    cur.execute(sql_oferece)
    con.commit()
    con.close()


"""
    def cad_loginProf():
        

    def cadastraClientes():
        cur.execute("INSERT INTO clientes (nome, cpf, telefone, email, rua, numero, cidade, bairro, cep, estado ) values('Marcelo', '088.617.184-93', '(87)9.81199151', 'devmarcelo.gus@gmail.com', 'rua João Gonçalves da SIlva', '115','Garanhuns', 'Boa Vista', '55292405', 'PE')")
        con.commit()

    
        
    def cadastraServicos():
        

    def cadastraCursos():
        cur.execute("INSERT INTO cursos (fk_idProfiss, modalidade, instituicao, area) VALUES(1, 'tecnico', 'ariano suassuna', 'informática')")
        con.commit()

    def cadastraExperiencia():
        cur.execute("INSERT INTO experiencias (fk_IDprofiss, cargo, temp_servico, empresa) VALUES(1, 'atendente', '1a', 'j.i lanhouse')")
        con.commit()

    cadastraClientes()
    cadastraProfissionais()
    cadastraServicos()
    cadastraCursos()
    cadastraExperiencia()
    cad_loginProf()
    con.close()
"""
