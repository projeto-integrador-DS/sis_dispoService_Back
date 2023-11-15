from flask import render_template, request, redirect, url_for, flash, Blueprint
import sqlite3 as sql
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_required, logout_user,login_user, current_user, UserMixin

clientes_blueprint = Blueprint('clientes', __name__, template_folder='templates')
login_manager = LoginManager()


#---------- Rota Inicial ----------
@clientes_blueprint.route('/')
def inicial():
    return render_template('inicial_01.html')


#---------- Rota Login Cliente ----------
@clientes_blueprint.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')

    return render_template('login.html')


#---------- Rota cliente escolha serviço ----------
@clientes_blueprint.route('/escolha_servico')
def escolhaServico():
    return render_template('escolha_servicos.html',dados="")


#---------- Rota Menu CLiente ----------
@clientes_blueprint.route('/menu_cliente')
def menu_cliente():
    return render_template('menu_cliente.html')



#---------- Rota Clientes Cadastrados ----------
@clientes_blueprint.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('cadastrados.html', dados=data)



#---------- Rota Cadastrar Cliente ----------
@clientes_blueprint.route('/cadastre-se', methods=['POST', 'GET'])
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
        return redirect(url_for('clientes.inicial'))
    return render_template('cad_cliente.html')


#---------- Rota Editar Cliente ----------
@clientes_blueprint.route('/edit_user/<string:idCli>', methods=['POST', 'GET'])
def edit_user(idCli):
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
        cur.execute("UPDATE clientes set nome=?, email=?, cpf=?, telefone=?, rua=?, numero=?, cidade=?, bairro=?, estado=?, cep=? WHERE ID_clientes=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, idCli))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('clientes.inicial'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * from clientes WHERE ID_clientes=?", (idCli))
    dados = cur.fetchone()
    return render_template('edit_cliente.html', dados=dados)



#---------- Rota Excluir Cliente ----------
@clientes_blueprint.route('/delete_user/<string:idCli>', methods=['GET'])
def delete_user(idCli):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE from clientes WHERE ID_clientes=?", (idCli))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('clientes.inicial'))


#====================== Criação da Rota que filtra profissionais por serviço ==========================
@clientes_blueprint.route('/profissionais/<profissao>', methods=['GET'])
def list_profissionais(profissao):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute(f'''
                SELECT * FROM profissionais
                JOIN experiencias ON profissionais.ID_profiss = experiencias.fk_IDprofiss
                WHERE experiencias.cargo = '{profissao}';
            ''')
    dados = cur.fetchall()
   # Obtém os nomes das colunas
    colunas = [column[0] for column in cur.description]

    # Converte os resultados para uma lista de dicionários
    dados_json = [dict(zip(colunas, row)) for row in dados]

    
    # Converte a lista de dicionários para JSON usando jsonify
    return render_template('perfil_profissional.html', profissionais=dados_json)

#=================Login Cliente=================
@login_manager.user_loader
def load_user(user_id):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (user_id,))
    user_cli = cur.fetchone()
    if not user_cli:
      
        return 
    
    return UserCliente(user_cli[1])


@clientes_blueprint.route('/login_cliente', methods=['POST', 'GET'])
#@login_required Estava sem, porém se adicionado causa erro no login do profissional 
def login_cliente():
    from profissionais.funcoes import  verificacao
    
    if request.method=='POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        return verificacao(username, senha)
    return render_template("login_cliente.html")

@clientes_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'



@clientes_blueprint.route('/protected')
@login_required
def protected():
    from profissionais.funcoes import get_id_cliente
    id_cli=get_id_cliente()    
    print(id_cli)
    return render_template('index.html', usuario=current_user.id, id_cli=id_cli)



class UserCliente(UserMixin):
    def __init__(self, id):
        self.id = id

