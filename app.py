from flask import Flask, jsonify
from flask_restful import Api
from resources.clientes import Cliente, Cliente_register, ClienteLogin,ClienteLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)


@app.before_request
def cria_banco():
    sa.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({"Mensagem": "Você foi desconectdado"}), 401



# Caminhos
#api.add_resource(Cliente, '/clientes')
api.add_resource(Cliente, '/clientes/<int:cliente_id>')
api.add_resource(Cliente_register, '/cadastro')
api.add_resource(ClienteLogin,'/login')
api.add_resource(ClienteLogout, '/logout')


# Inicializador
if __name__ == '__main__':
    from sql_alchemy import sa 
    sa.init_app(app)
    app.run(debug=True)