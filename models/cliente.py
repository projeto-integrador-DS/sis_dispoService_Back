from sql_alchemy import sa

class ClienteModel(sa.Model):
    __tablename__ = 'clientes'

    cliente_id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String(80))
    email = sa.Column(sa.String(40))
    cpf = sa.Column(sa.String(11))
    uf = sa.Column(sa.String(2))
    cidade = sa.Column(sa.String(40))
    bairro = sa.Column(sa.String(20))
    rua = sa.Column(sa.String(40))
    numero = sa.Column(sa.Integer)
    cep = sa.Column(sa.String(8))
    login = sa.Column(sa.String(40))
    senha = sa.Column(sa.String(40))

    def __init__(self, nome, email, cpf, uf, cidade, bairro, rua, numero, cep, login, senha):
        #self.cliente_id = cliente_id Para ficar auto incrementado o melhor é não passar no construtor o id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.uf = uf
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.cep = cep
        self.login = login
        self. senha = senha

    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'uf': self.uf,
            'cidade': self.cidade,
            'bairro': self.bairro,
            'rua': self.rua,
            'numero': self.numero,
            'cep': self.cep,
            'login': self.login
        }
    

    @classmethod
    def find_cliente(cls,cliente_id):
        cliente = cls.query.filter_by(cliente_id=cliente_id).first()
        if cliente:
            return cliente
        return None
    

    @classmethod
    def find_by_login(cls, login):
        cliente = cls.query.filter_by(login=login).first()
        if cliente:
            return cliente
        return None
    

    def save_cliente(self):
        sa.session.add(self)
        sa.session.commit()


    """def update_cliente(self, nome, email, cpf, uf, cidade, bairro, rua, numero, cep, login, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.uf = uf
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.cep = cep
        self.login = login
        self. senha = senha"""

    
    def delete_cliente(self):
        sa.session.delete(self)
        sa.session.commit() 
