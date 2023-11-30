import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, flash
from login import login_manager, bp_login
from profissional import bp_profissional
from curso import bp_curso
from experiencia import bp_experiencia
from servicos import bp_servicos
#from form_db import cur

app = Flask(__name__)
app.secret_key="daniel123"

login_manager.init_app(app)

app.register_blueprint(bp_login)
app.register_blueprint(bp_profissional)
app.register_blueprint(bp_curso)
app.register_blueprint(bp_experiencia)
app.register_blueprint(bp_servicos)

#---------- Rota Inicial ----------
@app.route('/')
def inicial():
    return render_template('inicial_01.html')


if __name__ == '__main__':
    app.run(debug=True)