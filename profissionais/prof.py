from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_login import LoginManager
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


prof_blueprint = Blueprint('prof', __name__, template_folder='templates')
login_manager = LoginManager()

#---------- Começo CRUD Profissionais ----------

@prof_blueprint.route('/index', methods=['POST', 'GET'])
def index():
    id_profiss=get_id_usuario()
    return render_template('index.html', id_profiss=id_profiss)

@prof_blueprint.route('/indexServico')
def indexServico():
    con=sql.connect("goservice.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM servicos")
    servico=cur.fetchall()

    return render_template('indexServicos.html', servicos=servico)


#============PROFISSIONAIS==============
@prof_blueprint.route('/cad_profissionais', methods=['POST', 'GET'])
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
        return redirect(url_for('prof.cad_profUser'))
 
    return render_template('cad_profissionais.html')


#======================Editar Profissionais=======================
@prof_blueprint.route('/edit_profissionais/<int:idProf>', methods=['POST', 'GET'])
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
        return redirect(url_for('prof.inicial')) #Lenbrar de mudar a rota
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (idProf,))
    data = cur.fetchone()
    return render_template('edit_profissionais.html', datas=data)


#================Deletar Profissionais==================
@prof_blueprint.route('/delete_profissionais/<int:idProf>', methods=['GET'])
def delete_profissionais(idProf):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID_profiss=?", (idProf,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('prof.edit_profissionais')) #Está indo para a rota editar profissional


#=====================CADASTRAR USERNAME E SENHA DO USUARIO=======================
@prof_blueprint.route('/cad_profUser', methods=['POST', 'GET'])
def cad_profUser():
    if request.method=='POST':
        username=request.form['username'].strip()
        senha=request.form['senha'].strip()
        con = sql.connect('goservice.db')
        senha_hash = generate_password_hash(senha)
        fk_idProfiss = getUltimoProfis()
        cur = con.cursor()
        cur.execute("INSERT INTO loginProf(fk_profiss, username, senha) VALUES (?,?,?)", (fk_idProfiss, username, senha_hash))
        con.commit()
        con.close()
        return redirect(url_for('prof.cad_curso'))
    return render_template('cad_profUser.html')


@login_manager.user_loader
def load_user(user_id):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (user_id,))
    user_prof = cur.fetchone()
    if not user_prof:
      
        return 
    
    return User_profiss(user_prof[1])


@prof_blueprint.route('/login_profissional', methods=['POST', 'GET'])
def login_profissional():
    
    if request.method=='POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        return verificacao(username, senha)
    return render_template("login_profissional.html")

@prof_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'



@prof_blueprint.route('/protected')
@login_required
def protected():
    id_profiss=get_id_usuario()    
    print(id_profiss)
    return render_template('index.html', usuario=current_user.id, id_profiss=id_profiss)


#============RELACIONA SERVIÇO COM PROFISSIONAL==============
def prof_serv(id_profiss):
    
    id_prof=id_profiss

    id_Serv=getUltimoServico()

    con=sql.connect('goservice.db')
    cur=con.cursor()
    
    cur.execute("INSERT INTO oferece (fk_profiss, fk_servic) values(?,?)", (id_prof, id_Serv))
    con.commit()
    con.close()

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


def get_id_usuario():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM loginProf WHERE username=?", (current_user.id,))
    id_profiss = cur.fetchone()
    return id_profiss[0]


def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

def getUltimoProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf

def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

class User_profiss(UserMixin):
    def __init__(self, id):
        self.id = id