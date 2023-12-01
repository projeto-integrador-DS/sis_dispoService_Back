import sqlite3 as sql
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, UserMixin, login_required, LoginManager
from flask import redirect, render_template, url_for, flash, Blueprint, request


bp_logincli = Blueprint("logincliente",__name__, template_folder='templates')

login_manager = LoginManager()

class UserCliente(UserMixin):
    def __init__(self, id):
        self.id = id

#=================Login Cliente=================
@login_manager.user_loader
def load_user(user_id):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginCli WHERE username=?", (user_id,))
    user_cli = cur.fetchone()
    if not user_cli:
        return None
    return UserCliente(user_cli[1])

@bp_logincli.route('/login_cliente', methods=['POST', 'GET'])
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
        return redirect(url_for('logincliente.protected'))
    flash('Login invalido', 'warning')
    return redirect(url_for('logincliente.login_cliente'))

    

@bp_logincli.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('clientes.inicial'))


@bp_logincli.route('/protected')
@login_required
def protected():
        
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



