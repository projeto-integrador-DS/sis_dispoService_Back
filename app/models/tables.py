from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes' # Nome da tabela do banco de dados

    id = db.column(db.Integer, primary_key=True, autoincremente=True)
    nome = db.column(db.String(50), nullalble=False)
    email = db.column(db.String(45), nullable=False, unique=True)
    cpf = db.column(db.String(11), nullable=False, unique=True)

    def __init__(self, id, nome, email, cpf):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return f"<Cliente {self.nome}>"
    

class EnderecoCli(db.Model):
    __tablename__ = 'endereco_cli'

    id = db.column(db.integer, primary_key= True, autoincrement=True)
    cliente_id = db.column(db.integer, db.ForeignKey('clientes.id'))
    uf = db.column(db.String(2), nullable=False)
    cidade = db.column(db.String(30), nullable=False)
    bairro = db.column(db.String(20), nullable=False)
    rua = db.column(db.String(50), nullable=False)
    cep = db.column(db.String(8), nullable=False)

    cliente = db.relationship('Cliente', Foreign_Keys=cliente_id)

    def __init__(self, cliente_id, uf, cidade, bairro, rua, cep):
        self.cliente_id = cliente_id
        self.uf = uf
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.cep = cep

    def __repr__(self):
        return f"<Endereco {self.uf}, {self.cidade}, {self.bairro}, {self.rua}, {self.cep}>"


class TelefoneCli(db.model):
    __tablename__ = 'telefone_cli'

    telefone = db.column(db.Integer, primarykey=True, autoincrement=True)
    cliente_id = db.column(db.Integer, db.ForeignKey('clientes.id'))

    cliente = db.relationship('Cliente', Foreign_keys=cliente_id)
    telefonecli = db.relationship('Cliente', Foreign_keys=cliente_id)

    def __init__(self, cliente_id):
        self.cliente_id = cliente_id

    def __repr__(self):
        return f"<Telefone {self.cliente_id}>"
    
