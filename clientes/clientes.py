from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_login import LoginManager
import sqlite3 as sql

clientes_blueprint = Blueprint('clientes', __name__, template_folder='templates')

#---------- Rota Inicial ----------
@clientes_blueprint.route('/')
def inicial():
    return render_template('inicial_01.html')


#---------- Rota Login Cliente ----------
@clientes_blueprint.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')

    return render_template('login.html')


#---------- Rota cliente escolha serviço ----------
@clientes_blueprint.route('/escolha_servico')
def escolhaServico():
    return render_template('escolha_servicos.html',dados="")


#---------- Rota Menu CLiente ----------
@clientes_blueprint.route('/menu_cliente')
def menu_cliente():
    return render_template('menu_cliente.html')



#---------- Rota Clientes Cadastrados ----------
@clientes_blueprint.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('cadastrados.html', dados=data)



#---------- Rota Cadastrar Cliente ----------
@clientes_blueprint.route('/cadastre-se', methods=['POST', 'GET'])
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
        return redirect(url_for('clientes.inicial'))
    return render_template('cad_cliente.html')


#---------- Rota Editar Cliente ----------
@clientes_blueprint.route('/edit_user/<string:idCli>', methods=['POST', 'GET'])
def edit_user(idCli):
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
        cur.execute("UPDATE clientes set nome=?, email=?, cpf=?, telefone=?, rua=?, numero=?, cidade=?, bairro=?, estado=?, cep=? WHERE ID_clientes=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, idCli))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('clientes.inicial'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * from clientes WHERE ID_clientes=?", (idCli))
    dados = cur.fetchone()
    return render_template('edit_cliente.html', dados=dados)



#---------- Rota Excluir Cliente ----------
@clientes_blueprint.route('/delete_user/<string:idCli>', methods=['GET'])
def delete_user(idCli):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE from clientes WHERE ID_clientes=?", (idCli))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('clientes.inicial'))


#====================== Criação da Rota que filtra profissionais por serviço ==========================
@clientes_blueprint.route('/profissionais/<profissao>', methods=['GET'])
def list_profissionais(profissao):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute(f'''
                SELECT * FROM profissionais
                JOIN experiencias ON profissionais.ID_profiss = experiencias.fk_IDprofiss
                WHERE experiencias.cargo = '{profissao}';
            ''')
    dados = cur.fetchall()
   # Obtém os nomes das colunas
    colunas = [column[0] for column in cur.description]

    # Converte os resultados para uma lista de dicionários
    dados_json = [dict(zip(colunas, row)) for row in dados]

    
    # Converte a lista de dicionários para JSON usando jsonify
    return render_template('perfil_profissional.html', profissionais=dados_json)
