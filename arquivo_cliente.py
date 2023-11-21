from flask import render_template, request, redirect, url_for, flash, Blueprint
import sqlite3 as sql

from flask_login import LoginManager, login_required, logout_user,login_user, current_user, UserMixin

bpclientes_blueprint = Blueprint('clientes', __name__)


#---------- Rota Inicial ----------
@bpclientes_blueprint.route('/')
def inicial():
    return render_template('clientes/inicial_01.html')


#---------- Rota cliente escolha serviço ----------
@bpclientes_blueprint.route('/escolha_servico')
def escolhaServico():
    from clientes.login_cli import get_id_cliente
    id_cli=get_id_cliente()
    return render_template('escolha_servicos.html',usuario=current_user.id, id_cli=id_cli)



#---------- Rota Clientes Cadastrados ----------
@bpclientes_blueprint.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('cadastrados.html', dados=data)



#---------- Rota Cadastrar Cliente ----------
@bpclientes_blueprint.route('/cadastre-se', methods=['POST', 'GET'])
def cadastra_cliente():
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
        return redirect(url_for('clientes.cad_profCli'))
    return render_template('clientes/cad_cliente.html')


#---------- Rota Editar Cliente ----------
@bpclientes_blueprint.route('/edit_user/<string:idCli>', methods=['POST', 'GET'])
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
        cur.execute("UPDATE clientes SET nome=?, email=?, cpf=?, telefone=?, rua=?, numero=?, cidade=?, bairro=?, estado=?, cep=? WHERE ID_clientes=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, idCli))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('clientes.inicial'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * from clientes WHERE ID_clientes=?", (idCli))
    dados = cur.fetchone()
    return render_template('clientes/edit_cliente.html', dados=dados)



#---------- Rota Excluir Cliente ----------
@bpclientes_blueprint.route('/delete_user/<string:idCli>', methods=['GET'])
def delete_user(idCli):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE from clientes WHERE ID_clientes=?", (idCli))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('clientes.inicial'))




#====================== Criação da Rota que filtra profissionais por serviço ==========================
@bpclientes_blueprint.route('/profissionais/<profissao>', methods=['GET'])
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

