from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Blueprint, redirect, render_template, url_for, request
import sqlite3 as sql
from form_db import setup 

login_manager = LoginManager()

bp_login = Blueprint('login', __name__)

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
        return redirect(url_for('login.protected'))
    return render_template('/profissional/login_profissional.html')

@bp_login.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'

@bp_login.route('/protected')
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