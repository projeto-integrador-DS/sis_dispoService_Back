from flask import Flask, jsonify
from flask_restful import Api
from resources.clientes import Cliente, Cliente_register, ClienteLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    sa.create_all()

#api.add_resource(Cliente, '/clientes')
api.add_resource(Cliente, '/clientes/<int:cliente_id>')
api.add_resource(Cliente_register, '/cadastro')
api.add_resource(ClienteLogin,'/login')


# Inicializador
if __name__ == '__main__':
    from sql_alchemy import sa 
    sa.init_app(app)
    app.run(debug=True)