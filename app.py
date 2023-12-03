import sqlite3 as sql
from flask import Flask
from profissional import bp_profissional
from curso import bp_curso
from experiencia import bp_experiencia
from servicos import bp_servicos
from login import bp_login, login_manager
from cliente import bp_clientes



app = Flask(__name__)


app.register_blueprint(bp_login)
app.register_blueprint(bp_profissional)
app.register_blueprint(bp_curso)
app.register_blueprint(bp_experiencia)
app.register_blueprint(bp_servicos)
app.register_blueprint(bp_clientes)


login_manager.init_app(app)

app.secret_key="daniel123"
