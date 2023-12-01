from flask import Flask

#------Importando o módulo cliente-----
from cliente import bpclientes_blueprint

#------Importando o módulo login-cliente------
from login_cli import bp_logincli

#------Importando a instancia login_manager------
from login_cli import login_manager

app = Flask(__name__)
login_manager.init_app(app)



app.register_blueprint(bpclientes_blueprint)
app.register_blueprint(bp_logincli)

app.secret_key="daniel123"


if __name__ == '__main__':
    app.run(debug=True)