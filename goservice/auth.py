from flask import Blueprint, render_template, request, url_for, redirect

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro/')
def cadastro():
   
    return render_template('cadastro.html')

@auth_bp.route('/cadastro/', methods=['GET', 'POST'])
def cadastro_post():
    nome_usuario = request.form.get('username')
    senha = request.form.get('password')
    print(nome_usuario, senha)

    return redirect(url_for('auth.login'))

@auth_bp.route('/login/', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@auth_bp.route('/logout/', methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')
