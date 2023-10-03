from flask.views import MethodView
from flask import request, render_template, redirect
from src.db import con, conecta



class IndexClientes(MethodView):
    def get(self):
        conecta()
        with con.cursor() as c:
            c.execute("SELECT * FROM clientes")
            data = c.fetchall()
            return render_template('/cadastro.html', data=data)
        
class CadClientes(MethodView):
    def post(self):
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        uf = request.form['uf']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        rua = request.form['rua']
        num_casa = request.form['num_casa']
        cep = request.form['cep']
        username = request.form['username']
        senha = request.form['senha']

        conecta()
        cursor = con.cursor()
        sql = 'INSERT INTO clientes (nome, email, telefone, cpf, uf, cidade, bairro, rua, num_casa, cep, username, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (nome, email, telefone, cpf, uf, cidade, bairro, rua, num_casa, cep, username, senha))

        con.commit()
        return redirect('/cadastro')
        