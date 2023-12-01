from flask import render_template, request, redirect, url_for, flash, Blueprint
import sqlite3 as sql
from flask_login import LoginManager, login_required, logout_user,login_user, current_user, UserMixin
from werkzeug.security import generate_password_hash

bpclientes_blueprint = Blueprint('clientes', __name__)


#---------- Rota Inicial ----------
@bpclientes_blueprint.route('/')
def inicial():
    return render_template('clientes/inicial_01.html')


#---------- Rota cliente escolha serviço ----------
@login_required
@bpclientes_blueprint.route('/escolha_servico')
def escolhaServico():
    from login_cli import get_id_cliente
    id_cli=get_id_cliente()
    return render_template('clientes/escolha_servicos.html',usuario=current_user.id, id_cli=id_cli)



#---------- Rota Clientes Cadastrados ----------
@bpclientes_blueprint.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('clientes/cadastrados.html', dados=data)



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
    return render_template('/clientes/cad_cliente.html')


#=====================CADASTRAR USERNAME E SENHA DO USUARIO CLIENTE=======================
@bpclientes_blueprint.route('/cad_profCli', methods=['POST', 'GET'])
def cad_profCli():
    if request.method=='POST':
        username=request.form['username'].strip()
        senha=request.form['senha'].strip()
        con = sql.connect('goservice.db')
        senha_hash = generate_password_hash(senha)
        fk_cli = getUltimoCli()
        cur = con.cursor()
        cur.execute("INSERT INTO loginCli(fk_cli, username, senha) VALUES (?,?,?)", (fk_cli, username, senha_hash))
        con.commit()
        con.close()
        return redirect(url_for('clientes.inicial'))
    return render_template('clientes/cad_CliUser.html')

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
        return redirect(url_for('logincliente.protected'))
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
    cur.execute("DELETE  from clientes WHERE ID_clientes=?", (idCli,))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('clientes.inicial'))




#====================== Criação da Rota que filtra profissionais por serviço ==========================
def obter_profissionais_por_profissao(profissao):
    try:
        with sql.connect("goservice.db") as con:
            cur = con.cursor()
            print(profissao)
            # Use parâmetros na consulta para evitar injeção de SQL
            cur.execute('''
                        SELECT * FROM profissionais
                        WHERE profissao = ?;
                    ''', (profissao,))

            dados = cur.fetchall()
            print('ggdgdgg',dados)
            # Obtém os nomes das colunas
            colunas = [column[0] for column in cur.description]

            # Converte os resultados para uma lista de dicionários
            dados_json = [dict(zip(colunas, row)) for row in dados]

            return dados_json

    except sql.Error as err:
        print(f"Erro ao executar a consulta: {err}")
        return None

# Exemplo de uso na rota
@bpclientes_blueprint.route('/profissionais/<profissao>', methods=['GET'])
def list_profissionais(profissao):
    profissionais = obter_profissionais_por_profissao(profissao)

    return render_template('clientes/perfil_profissional.html', profissionais=profissionais)

def getUltimoCli():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_clientes) FROM clientes;")
    id = cur.fetchone()
    idCli=id[0]
    con.close()
    return idCli