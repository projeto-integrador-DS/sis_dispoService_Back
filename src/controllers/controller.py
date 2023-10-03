from flask.views import MethodView
from flask import request, render_template, redirect
from src.db import con



class IndexClientes(MethodView):
    def get(self):      
        with con.cursor() as c:
            c.execute("SELECT * FROM clientes")
            data = c.fetchall()
            return render_template('public/cadastro.html', data=data)
        
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

        with con.cursor() as c:
            sql = 'INSERT INTO clientes (nome, email, telefone, cpf, uf, cidade, bairro, rua, num_casa, cep, username, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            c.execute(sql, (nome, email, telefone, cpf, uf, cidade, bairro, rua, num_casa, cep, username, senha))

            c.connection.commit()
            return redirect('/')
        