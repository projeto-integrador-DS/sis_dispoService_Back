from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager
import sqlite3 as sql

#------Importando o módulo cliente--------
from clientes.clientes import clientes_blueprint

#------Importando o módulo cliente--------
from profissionais.prof import prof_blueprint


app = Flask(__name__)

app.register_blueprint(clientes_blueprint)
app.register_blueprint(prof_blueprint)

app.secret_key="marcelo14"


if __name__ == '__main__':
    app.run(debug=True)
