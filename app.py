import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, flash
from login import login_manager, bp_login
from profissional import bp_profissional
from curso import bp_curso
from experiencia import bp_experiencia
from servicos import bp_servicos


app = Flask(__name__)
app.secret_key="daniel123"


#------Importando o módulo cliente-----
from cliente import bpclientes_blueprint

#------Importando o módulo login-cliente------
from login_cli import bp_logincli

#------Importando a instancia login_manager------
from login_cli import login_manager

app = Flask(__name__)
login_manager.init_app(app)

app.register_blueprint(bp_login)
app.register_blueprint(bp_profissional)
app.register_blueprint(bp_curso)
app.register_blueprint(bp_experiencia)
app.register_blueprint(bp_servicos)
app.register_blueprint(bpclientes_blueprint)
app.register_blueprint(bp_logincli)



if __name__ == '__main__':
    app.run(debug=True)