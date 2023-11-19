import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, flash
from login import login_manager, bp_login
from profissional import bp_profissional
from curso import bp_curso
from experiencia import bp_experiencia
from servicos import bp_servicos
#from form_db import cur

app = Flask(__name__)
app.secret_key="daniel123"

login_manager.init_app(app)

app.register_blueprint(bp_login)
app.register_blueprint(bp_profissional)
app.register_blueprint(bp_curso)
app.register_blueprint(bp_experiencia)
app.register_blueprint(bp_servicos)

#---------- Rota Inicial ----------
@app.route('/')
def inicial():
    return render_template('inicial_01.html')

#---------- Rota Login Cliente ----------
@app.route('/login_cliente')
def loginCliente():
    return render_template('login.html')

#---------- Rota Menu CLiente ----------
@app.route('/menu_cliente')
def menu_cliente():
    return render_template('menu_cliente.html')

#---------- Rota Clientes Cadastrados ----------
@app.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('cadastrados.html', datas=data)

#---------- Rota Cadastrar Cliente ----------
@app.route('/cadastre-se', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        nome =      request.form['nome']
        email =     request.form['email']
        cpf =       request.form['cpf']
        telefone =  request.form['telefone']
        rua =       request.form['rua']
        numero =    request.form['numero']
        cidade =    request.form['cidade']
        bairro =    request.form['bairro']
        estado =    request.form['estado']
        cep =       request.form['cep']

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("insert into clientes(NOME, EMAIL, CPF, TELEFONE, RUA, NUMERO, BAIRRO, CIDADE, ESTADO, CEP) values (?,?,?,?,?,?,?,?,?,?)", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('inicial'))
    return render_template('add_user.html')

#---------- Rota Editar Cliente ----------
@app.route('/edit_user/<string:id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        nome =      request.form['nome']
        email =     request.form['email']
        cpf =       request.form['cpf']
        telefone =  request.form['telefone']
        rua =       request.form['rua']
        numero =    request.form['numero']
        cidade =    request.form['cidade']
        bairro =    request.form['bairro']
        estado =    request.form['estado']
        cep =       request.form['cep']
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("update clientes set nome=?, email=?, cpf=?, telefone=?, rua=?, numero=?, cidade=?, bairro=?, estado=?, cep=?, where ID_clientes=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, id))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('inicial'))
    con = sql.connect("clientes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes where ID=?", (id))
    dados = cur.fetchone()
    return render_template('edit_user.html', dados=dados)




#---------- Rota Excluir Cliente ----------
@app.route('/delete_user/<string:id>', methods=['GET'])
def delete_user(id):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("delete from clientes where ID=?", (id))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('inicial'))

if __name__ == '__main__':
    app.run(debug=True)