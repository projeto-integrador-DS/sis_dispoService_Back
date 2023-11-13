from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from form_db import cur

app = Flask(__name__)
app.secret_key="daniel123"
login_manager = LoginManager() #para que serve?
login_manager.init_app(app)



#---------- Rota Inicial ----------
@app.route('/')
def inicial():
    return render_template('inicial_01.html')

#---------- Rota Login Cliente ----------
@app.route('/login_cliente')
def loginCliente():
    return render_template('login.html')

#---------- Rota Menu CLiente ----------
@app.route('/menu_cliente')
def menu_cliente():
    return render_template('menu_cliente.html')

#---------- Rota Clientes Cadastrados ----------
@app.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('cadastrados.html', datas=data)

#---------- Rota Cadastrar Cliente ----------
@app.route('/cadastre-se', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        nome =      request.form['nome']
        email =     request.form['email']
        cpf =       request.form['cpf']
        telefone =  request.form['telefone']
        rua =       request.form['rua']
        numero =    request.form['numero']
        cidade =    request.form['cidade']
        bairro =    request.form['bairro']
        estado =    request.form['estado']
        cep =       request.form['cep']

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("insert into clientes(NOME, EMAIL, CPF, TELEFONE, RUA, NUMERO, BAIRRO, CIDADE, ESTADO, CEP) values (?,?,?,?,?,?,?,?,?,?)", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('inicial'))
    return render_template('add_user.html')

#---------- Rota Editar Cliente ----------
@app.route('/edit_user/<string:id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        nome =      request.form['nome']
        email =     request.form['email']
        cpf =       request.form['cpf']
        telefone =  request.form['telefone']
        rua =       request.form['rua']
        numero =    request.form['numero']
        cidade =    request.form['cidade']
        bairro =    request.form['bairro']
        estado =    request.form['estado']
        cep =       request.form['cep']
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("update clientes set nome=?, email=?, cpf=?, telefone=?, rua=?, numero=?, cidade=?, bairro=?, estado=?, cep=?, where ID_clientes=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, id))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('inicial'))
    con = sql.connect("clientes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes where ID=?", (id))
    dados = cur.fetchone()
    return render_template('edit_user.html', dados=dados)




#---------- Rota Excluir Cliente ----------
@app.route('/delete_user/<string:id>', methods=['GET'])
def delete_user(id):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("delete from clientes where ID=?", (id))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('inicial'))
#---------- Fim CRUD Cliente ----------



#---------- Começo CRUD Profissionais ----------
#@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    id_profiss=get_id_usuario()
    return render_template('index.html', id_profiss=id_profiss)

#============PROFISSIONAIS==============

@app.route('/cad_profissionais', methods=['POST', 'GET'])
def cad_profissionais():
    if request.method == 'POST':
        nome =      request.form['nome']
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["cep"]
        uf =        request.form['uf']
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO profissionais(nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf) values(?,?,?,?,?,?,?,?,?,?)", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('cad_profUser'))
        #return render_template('cad_cursos.html', cadastro=True) 
 
    return render_template('cad_profissionais.html')


@app.route('/edit_profissionais/<int:idProf>', methods=['POST', 'GET'])
def edit_profissionais(idProf):
    
    if request.method == 'POST':
        nome =      request.form['nome']
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["cep"]
        cep =       request.form["cep"]
        uf =        request.form['uf']


        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE profissionais SET nome=?, cpf=?, telefone=?, email=?, endereco=?, cidade=?, num=?, bairro=?, cep=?, uf=? WHERE ID_profiss=?", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, idProf))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('index')) #ele não deve retorna para o index
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (idProf,))
    data = cur.fetchone()
    return render_template('edit_profissionais.html', datas=data)

@app.route('/delete_profissionais/<int:idProf>', methods=['GET'])
def delete_profissionais(idProf):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID_profiss=?", (idProf,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('index')) #ele deve retorna pra visualizado dos dados pessoais

@app.route('/cad_profUser', methods=['POST', 'GET'])
def cad_profUser():
    if request.method=='POST':
        username=request.form['username']
        senha=request.form['senha']
        con = sql.connect('goservice.db')
        senha_hash = generate_password_hash(senha)
        fk_idProfiss = getUltimoProfis()
        cur = con.cursor()
        cur.execute("INSERT INTO loginProf(fk_profiss, username, senha) VALUES (?,?,?)", (fk_idProfiss, username, senha_hash))
        con.commit()
        con.close()
        return redirect(url_for('cad_curso'))
    return render_template('cad_profUser.html')
  

class User_profiss(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    setup()
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (user_id,))
    user_prof = cur.fetchone()
    if not user_prof:
      
        return None
    
    return User_profiss(user_prof[1])

    
@app.route('/login_profissional', methods=['POST', 'GET'])
def login_profissional():
    
    if request.method=='POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        return verificacao(username, senha)
    return render_template("login_profissional.html")

def verificacao(username, senha):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (username,))
    user_prof = cur.fetchone()
    
    if user_prof and check_password_hash(user_prof[2], senha):
        usuario = User_profiss(username)
        login_user(usuario) #registra o usuário logado, cria uma sessão para o usuário
        return redirect(url_for('protected'))
    return render_template('login_profissional.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'

@app.route('/protected')
@login_required
def protected():
    id_profiss=get_id_usuario()    
    print(id_profiss)
    return render_template('index.html', usuario=current_user.id, id_profiss=id_profiss)

def get_id_usuario():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM loginProf WHERE username=?", (current_user.id,))
    id_profiss = cur.fetchone()
    return id_profiss[0]
#============CURSOS==============
@app.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    if request.method=='POST':
        modalidade  = request.form['modalidade']
        instituicao = request.form['instituicao']     
        area        = request.form['area']
        fk_idProf = getUltimoProfis()
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (fk_idProf,modalidade, instituicao, area))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('cad_experiencia'))
    return render_template('cad_cursos.html', cadastro =True)

@app.route('/listacursos/')
def list_cursos_prof():
    id_profiss= get_id_usuario()
    print("função list_cursos_prof", id_profiss)
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (id_profiss,))
    cursos = cur.fetchall()      
    return render_template('lista_cursos.html', curs=cursos)

@app.route('/incluir_curso', methods=['POST', 'GET'])
def incluir_curso():
    id_profiss =get_id_usuario()
    print("chegou no incluir_curso:", id_profiss)
    if request.method=='POST':
        modalidade  = request.form['modalidade']
        instituicao = request.form['instituicao']     
        area        = request.form['area']
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        
        cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (id_profiss,modalidade, instituicao, area))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('list_cursos_prof'))
    return render_template('cad_cursos.html', cadastro = False, id_profiss=id_profiss)
    
@app.route("/edit_curso/<id_curso>", methods=["POST", "GET"])
def edit_curso(id_curso):
    
    if request.method == 'POST':
        modalidade =    request.form['modalidade']
        instituicao =   request.form["instituicao"]
        area =          request.form["area"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE cursos SET modalidade=?, instituicao=?, area=? WHERE ID_curso=?", (modalidade, instituicao, area, id_curso))
        con.commit()
        flash('Dados atualizados', 'success')
        #id_profiss = get_id_usuario()
        return redirect(url_for('list_cursos_prof'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE c.ID_curso =?", (id_curso,)) 
    #cur.execute("SELECT * FROM cursos WHERE ID_curso=?", (idCurso,))
    curso = cur.fetchone()
    return render_template('edit_cursos.html', cursos=curso)

@app.route('/delete_curso/<int:id_curso>', methods=['GET'])
def delete_curso(id_curso):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE ID_curso=?", (id_curso,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('list_cursos_prof'))

def getUltimoProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf

#============EXPERIÊNCIAS==============
@app.route('/experiencia', methods=['POST', 'GET'])
def cad_experiencia():
    if request.method == 'POST':
        cargo       = request.form['cargo']
        temp_servico = request.form['temp_servico']
        empresa     = request.form['empresa']

        fk_idProf   = getUltimoProfis()

        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO experiencias(fk_IDprofiss, cargo, temp_servico, empresa) values(?,?,?,?)", (fk_idProf,cargo, temp_servico, empresa))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('cad_servicos'))
    return render_template('cad_experiencias.html', cadastro=True)

@app.route('/lista_experiencias')
def lista_experiencias():
    id_profiss=get_id_usuario()
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT ID_experiencia, exp.cargo, exp.temp_servico, exp.empresa FROM experiencias AS exp JOIN profissionais AS pr ON pr.ID_profiss = exp.fk_IDprofiss WHERE pr.ID_profiss =?", (id_profiss,))
    experiencias = cur.fetchall()
    return render_template('lista_experiencias.html', exper=experiencias, id_profiss=id_profiss)

@app.route('/add_exper', methods=['POST', 'GET'])
def add_experiencia():
    id_profiss=get_id_usuario()
    if(request.method == 'POST'):
        cargo       = request.form['cargo']
        temp_servico = request.form['temp_servico']
        empresa     = request.form['empresa']
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO experiencias(fk_IDprofiss, cargo, temp_servico, empresa) values(?,?,?,?)", (id_profiss,cargo, temp_servico, empresa))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        
        return redirect(url_for('lista_experiencias'))
    return render_template('cad_experiencias.html', cadastro=False)
   
@app.route('/edit_experiencias/<int:idExperiencia>', methods=["POST", "GET"])
def edit_experiencias(idExperiencia):
    
    if request.method == 'POST':
        cargo =      request.form['cargo']
        tempoServico =       request.form["temp_servico"]
        empresa =  request.form["empresa"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE experiencias SET cargo=?, temp_servico=?, empresa=? WHERE ID_experiencia=?", (cargo, tempoServico, empresa, idExperiencia))
        con.commit()
        flash('Dados atualizados', 'success')
        id_profiss=get_id_usuario()
        return redirect(url_for('lista_experiencias', id_profiss=id_profiss))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    experiencia = cur.fetchone()
    return render_template('edit_experiencias.html', exper=experiencia)

@app.route('/delete_experiencia/<int:idExperiencia>', methods=['GET'])
def delete_experiencia(idExperiencia):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    con.commit()
    con.close()
    flash('Dados deletados', 'warning')
    id_profiss=get_id_usuario()
    return redirect(url_for('lista_experiencias', id_profiss=id_profiss))

#============SERVIÇOS==============
@app.route('/cad_servicos', methods=['POST', 'GET'])
def cad_servicos():
    if request.method=='POST':
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']
        
        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        #pega o ultimo id do profissional cadastrado
        ultimIDprof=getUltimoProfis()
        prof_serv(ultimIDprof)
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('login_profissional'))
    return render_template('cad_servicos.html', cadastro=True)

@app.route('/listaservicos', methods=['POST', 'GET'])
def lista_servicos():
    id_profiss=get_id_usuario()
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row
   
    cur.execute(" SELECT serv.ID_servico, serv.nome, serv.categoria, serv.valor FROM oferece AS o JOIN profissionais AS pr on o.fk_profiss=pr.ID_profiss JOIN servicos AS serv ON o.fk_servic = serv.ID_servico WHERE o.fk_profiss=?", (id_profiss,))
    servicos=cur.fetchall()
    con.close()
    return render_template('lista_servicos.html', serv=servicos)

@app.route('/add_servicos', methods=['POST', 'GET'])
def add_servicos():
    id_profiss=get_id_usuario()
    if request.method=='POST': 
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']

        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        
        prof_serv(id_profiss) #relaciona as tabelas servicos e profissionais

        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('lista_servicos'))
    return render_template('cad_servicos.html', cadastro=False)

@app.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
def edit_servicos(idServico):
    if request.method=='POST':
        nome=request.form['nome']
        categoria=request.form['categoria']
        valor=request.form['valor']

        con = sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("UPDATE servicos SET nome=?, categoria=?, valor=? WHERE ID_servico=?",(nome, categoria, valor, idServico))
        con.commit()
        id_profiss=get_id_usuario()
        return redirect(url_for('lista_servicos', id_profiss=id_profiss))
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row

    cur.execute("SELECT * FROM servicos WHERE ID_servico=?", (idServico,))
    servico =cur.fetchone()
    return render_template('edit_servicos.html', serv=servico)


#---------- Rota Excluir Serviços ----------
@app.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    id_profiss=get_id_usuario()
    return redirect(url_for('lista_servicos', id_profiss=id_profiss))

def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

#============RELACIONA SERVIÇO COM PROFISSIONAL==============
def prof_serv(id_profiss):
    
    id_prof=id_profiss
    #temos um func1 e func2 se o func2 salvar um serviço antes do func1 o func1 terá salvo um serviço do func2
    id_Serv=getUltimoServico()

    con=sql.connect('goservice.db')
    cur=con.cursor()
    
    cur.execute("INSERT INTO oferece (fk_profiss, fk_servic) values(?,?)", (id_prof, id_Serv))
    con.commit()
    con.close()

def setup():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
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
        "uf"        TEXT
        )'''
    


    sql_cursos = '''CREATE TABLE IF NOT EXISTS "cursos"(
        "ID_curso" INTEGER PRIMARY KEY AUTOINCREMENT,
        "fk_idProfiss"    INTEGER,
        "modalidade"    TEXT,
        "instituicao"   TEXT,
        "area"          TEXT,
        FOREIGN KEY ("fk_idProfiss") REFERENCES "profissionais" ("ID_profiss")
    )'''


    sql_experiencias='''CREATE TABLE IF NOT EXISTS "experiencias"(
        "ID_experiencia" INTEGER PRIMARY KEY AUTOINCREMENT,
        "fk_IDprofiss"    INTEGER,
        "cargo"         TEXT,
        "temp_servico"  TEXT,
        "empresa"       TEXT,
        FOREIGN KEY ("fk_IDprofiss") REFERENCES "profissionais" ("ID_profiss")
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
        FOREIGN KEY ("fk_profiss") REFERENCES "profissionais" ("ID_profiss"),
        FOREIGN KEY ("fk_servic") REFERENCES "servicos" ("ID_servico")
    )'''

    sql_login='''CREATE TABLE IF NOT EXISTS "loginProf"(
        "fk_profiss" INTEGER,
        "username"  TEXT,
        "senha"     TEXT,
        FOREIGN KEY ("fk_profiss") REFERENCES "profissionais" ("ID_profiss")
    )
    '''

    cur.execute(sql_login)
    cur.execute(sql_clientes)
    cur.execute(sql_profissionais)
    cur.execute(sql_cursos)
    cur.execute(sql_experiencias)
    cur.execute(sql_servicos)
    cur.execute(sql_oferece)
    con.commit()
    
"""
    def cad_loginProf():
        senhaHash=generate_password_hash("123")
        cur.execute("INSERT INTO loginProf (fk_profiss, username, senha) VALUES (?,?,?)", (1, 'Daniel', senhaHash))
        con.commit()

    def cadastraClientes():
        cur.execute("INSERT INTO clientes (nome, cpf, telefone, email, rua, numero, cidade, bairro, cep, estado ) values('Marcelo', '088.617.184-93', '(87)9.81199151', 'devmarcelo.gus@gmail.com', 'rua João Gonçalves da SIlva', '115','Garanhuns', 'Boa Vista', '55292405', 'PE')")
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

    cadastraClientes()
    cadastraProfissionais()
    cadastraServicos()
    cadastraCursos()
    cadastraExperiencia()
    cad_loginProf()
    con.close()
"""
if __name__ == '__main__':
    app.run(debug=True)