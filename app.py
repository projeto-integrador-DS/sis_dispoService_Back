import sqlite3 as sql
from flask import Flask
from login import login_manager, bp_login
from profissional import bp_profissional
from curso import bp_curso
from experiencia import bp_experiencia
from servicos import bp_servicos
from cliente import bpclientes_blueprint
from login_cli import bp_logincli, login_manager_cliente


app = Flask(__name__)

login_manager.init_app(app)
login_manager_cliente.init_app(app)

app.register_blueprint(bp_login)
app.register_blueprint(bp_profissional)
app.register_blueprint(bp_curso)
app.register_blueprint(bp_experiencia)
app.register_blueprint(bp_servicos)
app.register_blueprint(bpclientes_blueprint)
app.register_blueprint(bp_logincli)

app.secret_key="daniel123"

if __name__ == '__main__':
    app.run(debug=True)