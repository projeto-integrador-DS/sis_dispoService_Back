from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro/')
def cadastro():
    return render_template('cadastro.html')

@auth_bp.route('/login/')
def login():
    return render_template('login.html')

@auth_bp.route('/logout/')
def logout():
    return render_template('logout.html')
