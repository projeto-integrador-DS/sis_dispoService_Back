from flask_restful import Resource,reqparse
from models.cliente import ClienteModel
from secrets import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

atributos = reqparse.RequestParser()
"""atributos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ficar em branco!")
atributos.add_argument('email', type=str, required=True, help="O ccampo 'email' não pode ficar em branco!")
atributos.add_argument('cpf', type=str, required=True, help="O campo 'cpf' não pode ficar em branco!")
atributos.add_argument('uf', type=str, required=True, help="O campo 'uf' não pode ficar em branco!")
atributos.add_argument('cidade', type=str, required=True, help="O campo 'cidade' não pode ficar em branco!")
atributos.add_argument('bairro', type=str, required=True, help="O campo 'bairro' não pode ficar em branco!")
atributos.add_argument('rua', type=str, required=True, help="O campo 'rua' não pode ficar em branco!")
atributos.add_argument('numero', type=int, required=True, help="O campo 'numero' não pode ficar em branco!")
atributos.add_argument('cep', type=str, required=True, help="O campo 'cep' não pode ficar em branco!")"""
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ficar em branco!")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ficar em branco!")


class Cliente(Resource):
    #/clientes/cliente_id

    def get(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            return cliente.json()
        return {'mensagem': 'Cliente não encontrado.'}, 404
    
    @jwt_required()
    def delete(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            try:
                cliente.delete_cliente()
            except:
                return {'Mensagem': 'Cliente deletado.'}
            return {'Mensagem': 'Cliente não encontrado.'}, 404
        return {"Messagem": "Usuário não encontrado"}

class Cliente_register(Resource):
    # endpoint /cadastro

    def post(self):
        dados = atributos.parse_args()

        if ClienteModel.find_by_login(dados['login']):
            return {"Mensagem": f"O usuário{dados['login']} já existe"}
        
        cliente = ClienteModel(**dados)
        cliente.save_cliente()
        return {'Messagem': 'Cliente criado com sucesso!'}, 201

class ClienteLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        cliente = ClienteModel.find_by_login(dados['login'])

        if cliente and compare_digest(cliente.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=cliente.cliente_id)
            return {"access_token": token_de_acesso}, 200
        return {"Messagem": "Nome de usuário ou senha incorretos"}, 401
