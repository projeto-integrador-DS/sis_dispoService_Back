from flask import render_template, request, redirect, url_for, flash, Blueprint
import sqlite3 as sql
from flask_login import  login_required, current_user
from werkzeug.security import generate_password_hash

bp_clientes = Blueprint('clientes', __name__)


#---------- Rota Inicial ----------
@bp_clientes.route('/')
def inicial():
    return render_template('clientes/inicial_01.html')



#---------- Rota cliente escolha serviço ----------
@login_required
@bp_clientes.route('/escolha_servico')
def escolhaServico():
    from login import get_id_cliente
    id_cli=get_id_cliente()
    return render_template('clientes/escolha_servicos.html',usuario=current_user.id, id_cli=id_cli)



#---------- Rota Clientes Cadastrados ----------
@bp_clientes.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from clientes")
    data = cur.fetchall()
    return render_template('clientes/cadastrados.html', dados=data)


#---------- Rota Meus Dados Cadastrais ----------
@bp_clientes.route('/visual_cliente')
def visual_cliente():
    from login import get_id_cliente
    con=sql.connect('goservice.db')
    cur=con.cursor()
    con.row_factory=sql.Row
    id_cliente = get_id_cliente()
    consulta = '''  SELECT cli.ID_clientes, cli.nome, cli.cpf, cli.telefone, cli.email, cli.rua, cli.numero, cli.bairro, cli.cep, cli.cidade, cli.estado
                    FROM clientes AS cli 
                    WHERE cli.ID_clientes=?'''
    cur.execute(consulta, (id_cliente,))
    cliente = cur.fetchone()
    
    con.close()
    return render_template('/clientes/visual_cliente.html', datas=cliente)




#---------- Rota Cadastrar Cliente ----------
@bp_clientes.route('/cadastre-se', methods=['POST', 'GET'])
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
@bp_clientes.route('/cad_profCli', methods=['POST', 'GET'])
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
@bp_clientes.route('/edit_user/<string:idCli>', methods=['POST', 'GET'])
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
        return redirect(url_for('clientes.visual_cliente'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * from clientes WHERE ID_clientes=?", (idCli))
    dados = cur.fetchone()
    return render_template('clientes/edit_cliente.html', dados=dados)



#---------- Rota Excluir Cliente ----------
@bp_clientes.route('/delete_user/<string:idCli>', methods=['GET'])
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
            cur.execute('''
                        SELECT * FROM profissionais
                        WHERE profissao = ?;
                    ''', (profissao,))

            dados = cur.fetchall()
            # Obtém os nomes das colunas
            colunas = [column[0] for column in cur.description]

            # Converte os resultados para uma lista de dicionários
            dados_json = [dict(zip(colunas, row)) for row in dados]

            return dados_json

    except sql.Error as err:
        print(f"Erro ao executar a consulta: {err}")
        return None


@bp_clientes.route('/profissionais/<profissao>', methods=['GET'])
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