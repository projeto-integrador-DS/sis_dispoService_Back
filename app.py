from flask import Flask
import sqlite3 as sql
from flask_login import LoginManager

from flask_ngrok import run_with_ngrok

#------Importando o módulo cliente--------
from clientes.clientes import clientes_blueprint

#------Importando o módulo profissional--------
from profissionais.prof import prof_blueprint

#------Importando o módulo experiencia--------
from profissionais.expe import expe_blueprint

#------Importando o módulo servicos--------
from profissionais.serv import serv_blueprint

#------Importando o módulo cursos--------
from profissionais.cursos import cursos_blueprint


app = Flask(__name__)
run_with_ngrok(app)
app.secret_key="daniel123"

login_manager = LoginManager(app)
login_manager.init_app(app)


app.register_blueprint(clientes_blueprint)
app.register_blueprint(prof_blueprint)
app.register_blueprint(expe_blueprint)
app.register_blueprint(serv_blueprint)
app.register_blueprint(cursos_blueprint)





if __name__ == '__main__':
    
    app.run(debug=True)