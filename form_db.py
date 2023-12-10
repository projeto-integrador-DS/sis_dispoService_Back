import sqlite3 as sql
def setup():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    con = sql.connect('goservice.db', detect_types=sql.PARSE_DECLTYPES)
    con.execute('PRAGMA foreign_keys = ON')

    sql_clientes = '''CREATE TABLE IF NOT EXISTS "clientes"(
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

import sqlite3
from faker import Faker
import random
from werkzeug.security import generate_password_hash

fake = Faker()

def profiss_ficticios():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()
    profissoes=('pintor', 'pedreiro', 'encanador', 'cuidador')

    i=0
    for _ in range(20):
        
        nome = fake.name()
        cpf = fake.unique.random_number(11)
        telefone = fake.phone_number()
        email = fake.email()

        endereco = fake.street_name()
        num = fake.building_number()
        bairro = fake.city_suffix()
        cep = fake.zipcode()
        cidade = fake.city()
        uf = "PE"
        if i<4:
            profissao=profissoes[i]
        else:
            i=0
            profissao=profissoes[i]
    
        print(profissao)
        cursor.execute(f"INSERT INTO profissionais( nome, CPF, telefone, email, endereco, num, bairro, CEP, cidade, uf, profissao) VALUES('{nome}', '{cpf}', '{telefone}', '{email}', '{endereco}', '{num}', '{bairro}', '{cep}', '{cidade}', '{uf}', '{profissao}')")
        conn.commit()
        i+=1

def loginProf_ficticio():
    #logins para os profissionais de 77 - 96
    #pega todos os nomes de usuário e pega o primeiro nome para no nome de usuário
    #e a senha 123 para todos
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ID_profiss, nome FROM profissionais')
    dados=cursor.fetchall()
   
    for dado in dados:
        fk_profiss=dado[0]
        username=dado[1].split()[0]
        senha =generate_password_hash('123')
        
        cursor.execute(f"INSERT INTO loginProf(fk_profiss, username, senha) VALUES('{fk_profiss}', '{username}', '{senha}')")
        conn.commit()      


def cursos_ficticio():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID_profiss FROM profissionais')
    ids=cursor.fetchall()

    for id in ids:
        fk_idProfiss=id[0]
        modalidade =modalidade = fake.random_element(elements=('profissionalizante', 'Técnico', 'Superior', 'especialização'))
        instituicao = fake.company()
        area = fake.job()
        cursor.execute(f"INSERT INTO cursos (fk_idProfiss, modalidade, instituicao, area) VALUES('{fk_idProfiss}', '{modalidade}', '{instituicao}', '{area}')")
        conn.commit()

#-----------------------ALIMENTANDO O SISTEMA COM 5 LINHAS CADA, DE CURSOS, EXPERIÊNCIAS E SERVIÇOS PARA UM PROFISSIONAL ESPECÍFICO (Robin e Lauren)-------------------------------------------------

def novosCadastros():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()
    #oferece
    cursor.execute(f"INSERT INTO oferece (fk_profiss, fk_servic) VALUES(?,?), (?,?), (?,?), (?,?), (?,?)",
                   (95,34, 95,35, 95,36, 95,37, 95,38))
    conn.commit()
    #serviços
    for _ in range(5):
        nome = fake.word()
        categoria = fake.random_element(elements=('construção', 'limpeza', 'manutenção'))
        valor = fake.random.uniform(50, 200)

        cursor.execute(f"INSERT INTO servicos (nome, categoria, valor) VALUES ('{nome}', '{categoria}', '{valor}')")
        conn.commit()
    #experiencias
    for _ in range(5):
        fk_IDprofiss=95
        cargo = fake.job()
        temp_servico = fake.random_element(elements=('2a 6m', '3a', '1a', '10a', '20a', '4a', '7a', '12a', '5a'))
        empresa = fake.company()

        cursor.execute(f"INSERT INTO experiencias (fk_IDprofiss, cargo, temp_servico, empresa) VALUES ('{fk_IDprofiss}', '{cargo}', '{temp_servico}', '{empresa}')")
        conn.commit()
    #cursos
    for _ in range(5):
        fk_idProfiss=95
        modalidade = fake.random_element(elements=('profissionalizante', 'Técnico', 'Superior', 'especialização'))
        instituicao = fake.company()
        area = fake.job()
        cursor.execute(f"INSERT INTO cursos (fk_idProfiss, modalidade, instituicao, area) VALUES('{fk_idProfiss}', '{modalidade}', '{instituicao}', '{area}')")
        conn.commit()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def experiencia_ficticia():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ID_profiss FROM profissionais')
    ids=cursor.fetchall()

    for id in ids:
        fk_IDprofiss=id[0]
        cargo = fake.job()
        temp_servico = fake.random_element(elements=('2a 6m', '3a', '1a', '10a', '20a', '4a', '7a', '12a', '5a'))
        empresa = fake.company()

        cursor.execute(f"INSERT INTO experiencias (fk_IDprofiss, cargo, temp_servico, empresa) VALUES ('{fk_IDprofiss}', '{cargo}', '{temp_servico}', '{empresa}')")
        conn.commit()


def servico_ficticio():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()

    for _ in range(20):
        nome = fake.word()
        categoria = fake.random_element(elements=('construção', 'limpeza', 'manutenção'))
        valor = fake.random.uniform(50, 200)

        cursor.execute(f"INSERT INTO servicos (nome, categoria, valor) VALUES ('{nome}', '{categoria}', '{valor}')")
        conn.commit()

def oferece_ficticio():
    conn = sqlite3.connect('goservice.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ID_profiss  FROM profissionais")
    profissionais=cursor.fetchall()
    
    cursor.execute("SELECT ID_servico  FROM servicos")
    servicos=cursor.fetchall()

    lista_id_prof=[]
    lista_id_serv=[]
    for id_prof in profissionais:
       
        lista_id_prof.append(id_prof[0])
      
    for id_serv in servicos:
        lista_id_serv.append(id_serv[0])
        
    for i in range(21):
        print(lista_id_prof[i])
        cursor.execute(f"INSERT INTO oferece (fk_profiss, fk_servic) VALUES ('{lista_id_prof[i]}','{lista_id_serv[i]}')")
        conn.commit()


def chama_Funcoes():
    #alimentando com dados 1 para 1
    oferece_ficticio()
    servico_ficticio()
    experiencia_ficticia()
    cursos_ficticio()
    loginProf_ficticio()

    #cadastro para profissional específico 1:N
    novosCadastros()
