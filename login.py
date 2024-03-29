from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Blueprint, redirect, render_template, url_for, request,flash
import sqlite3 as sql

#cria um objeto login_manager
login_manager = LoginManager()

bp_login = Blueprint('login', __name__)

class User_profiss(UserMixin):
    def __init__(self, idprof):
        self.id = idprof

class UserCliente(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    # Tenta carregar como usuário profissional
    cur.execute("SELECT * FROM loginProf WHERE username=?", (user_id,))
    user_prof = cur.fetchone()
    
    if user_prof:
        return User_profiss(user_prof[1])
    
    # Tenta carregar como usuário cliente
    cur.execute("SELECT * FROM loginCli WHERE username=?", (user_id,))
    user_cli = cur.fetchone()
    
    if user_cli:
        return UserCliente(user_cli[1])
    
    # Se nenhum usuário for encontrado, retorna None
    return None
    
@bp_login.route('/login_profissional', methods=['POST', 'GET'])
def login_profissional():    
    if request.method=='POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        return verificacao(username, senha)
    return render_template("/profissional/login_profissional.html")


def verificacao(username, senha):
    
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (username,))
    user_prof = cur.fetchone()
    
    if user_prof and check_password_hash(user_prof[2], senha):
        usuario = User_profiss(username)
        login_user(usuario) #registra o usuário logado, cria uma sessão para o usuário
        print(usuario)
        return redirect(url_for('login.protected'))
    flash('Login invalido', 'warning')
    return render_template('/profissional/login_profissional.html')

@bp_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('clientes.inicial'))

@bp_login.route('/protected', methods=["GET"])
@login_required
def protected():
    
    id_profiss = get_id_usuario()   

    #return render_template("/bases/base_index_profiss.html")
    
    return render_template('/bases/base_index_profiss.html', usuario=current_user.id, id_profiss=id_profiss)

def get_id_usuario():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM loginProf WHERE username=?", (current_user.id,))
    id_profiss = cur.fetchone()
    print(id_profiss)
    return id_profiss[0]



@bp_login.route('/login_cliente', methods=['POST', 'GET'])
def login_cliente():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        return verificacaoCli(username, senha)
        
    return render_template("clientes/login_cliente.html")



def verificacaoCli(username, senha):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginCli WHERE username=?", (username,))
    user_cli = cur.fetchone()
    
    if user_cli and check_password_hash(user_cli[2], senha):
        usuario = UserCliente(username)
        login_user(usuario) #registra o usuário logado, cria uma sessão para o usuário
        return redirect(url_for('login.protectedCli'))
    flash('Login invalido', 'warning')
    return redirect(url_for('login.login_cliente'))

    


@bp_login.route('/protected_cli')
@login_required
def protectedCli():
        
    # O usuário está autenticado, é seguro acessar current_user.id
    id_cliente = get_id_cliente()
    
    print(id_cliente)
    return render_template('/clientes/escolha_servicos.html', usuario=current_user.id, id_cliente=id_cliente)


def get_id_cliente():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM loginCli WHERE username=?", (current_user.id,))
    id_cli = cur.fetchone()
    return id_cli[0]
