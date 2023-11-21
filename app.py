from flask import Flask
from flask_login import LoginManager

#------Importando o módulo cliente-----
from arquivo_cliente import bpclientes_blueprint
#------Importando o módulo login-cliente------
from clientes.login_cli import bp_logincli


app = Flask(__name__)



def cria_blueprint():
    app.register_blueprint(bpclientes_blueprint)
    app.register_blueprint(bp_logincli)

app.secret_key="daniel123"


if __name__ == '__main__':
    cria_blueprint()  
    app.run(debug=True)