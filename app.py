from flask import Flask
from flask_login import LoginManager
from profissionais.prof import login_manager

#------Importando o módulo cliente--------
from clientes.clientes import clientes_blueprint

#------Importando o módulo login-cliente------
from clientes.login_cli import bp_logincli

#------Importando o módulo profissional--------
from profissionais.prof import prof_blueprint

#------Importando o módulo experiencia--------
from profissionais.expe import expe_blueprint

#------Importando o módulo servicos--------
from profissionais.serv import serv_blueprint

#------Importando o módulo cursos--------
from profissionais.cursos import cursos_blueprint


app = Flask(__name__)
login_manager.init_app(app)



#login_manager = LoginManager(app)

def cria_blueprint():
    app.register_blueprint(clientes_blueprint)
    app.register_blueprint(prof_blueprint)
    app.register_blueprint(expe_blueprint)
    app.register_blueprint(serv_blueprint)
    app.register_blueprint(cursos_blueprint)
    app.register_blueprint(bp_logincli)

app.secret_key="daniel123"


if __name__ == '__main__':
    cria_blueprint()  
    app.run(debug=True)