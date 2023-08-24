from app import db

class clientes(db.Model):
    __tablename__ = 'clientes' # Nome da tabela do banco de dados

    id = db.column(db.Integer, primary_key=True)
    nome = db.column(db.String(50), nullalble=False)
    email = db.column(db.String(45), nullable=False, unique=True)
    cpf = db.column(db.String(11), nullacle=False, unique=True)

    def __init__(self, id, nome, email, cpf):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return '<User %r>'% self.nome