from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import sqlite3 as sql
from login import get_id_usuario
from form_db import setup

bp_profissional=Blueprint('profissional',__name__)

#acho acho que podemos excluir essa rota
@bp_profissional.route('/index', methods=['POST', 'GET'])
def index():
    id_profiss=get_id_usuario()
    return render_template('bases/base_index_profiss.html', id_profiss=id_profiss)

#============PROFISSIONAIS==============
@bp_profissional.route('/')
def inicial():
    return render_template('clientes/inicial_01.html')

@bp_profissional.route('/cad_profissionais', methods=['POST', 'GET'])
def cad_profissionais():
    setup()
    if request.method == 'POST':
        nome =      request.form['nome']
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["cep"]
        uf =        request.form['uf']
        profissao=  request.form["profissao"]
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO profissionais(nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, profissao) values(?,?,?,?,?,?,?,?,?,?,?)", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, profissao))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('profissional.cad_profUser'))
       
 
    return render_template('/profissional/cad_profissionais.html')


@bp_profissional.route('/edit_profissionais/<idProf>', methods=['POST', 'GET'])
def edit_profissionais(idProf):
    
    if request.method == 'POST':
        nome =      request.form['nome']
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["cep"]
        uf =        request.form['uf']
        profissao = request.form['profissao']

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE profissionais SET nome=?, cpf=?, telefone=?, email=?, endereco=?, cidade=?, num=?, bairro=?, cep=?, uf=?, profissao=? WHERE ID_profiss=?", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, profissao, idProf))
        con.commit()
        con.close()
        flash('Dados atualizados', 'success')
        return redirect(url_for('profissional.visual_profissional'))
    
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (idProf,))
    data = cur.fetchone()
    
    return render_template('/profissional/edit_profissionais.html', datas=data)

@bp_profissional.route('/delete_profissionais', methods=['GET'])
def delete_profissionais():
    idProf=get_id_usuario()
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID_profiss=?", (idProf,))
    con.commit()
    con.close()
    flash('Dados deletados', 'warning')
    
    return redirect('/')


@bp_profissional.route('/cad_profUser', methods=['POST', 'GET'])
def cad_profUser():
    if request.method=='POST':
        username=request.form['username']
        senha=request.form['senha']
        con = sql.connect('goservice.db')
        senha_hash = generate_password_hash(senha)
        fk_idProfiss = getUltimoProfis()
        cur = con.cursor()
        cur.execute("INSERT INTO loginProf(fk_profiss, username, senha) VALUES (?,?,?)", (fk_idProfiss, username, senha_hash))
        con.commit()
        con.close()
        return render_template('/curso/cad_cursos.html', cadastro =True)
        #return redirect(url_for('cad_curso'))
    return render_template('/profissional/cad_profUser.html')

@bp_profissional.route('/visual_profissional')
def visual_profissional():
    con=sql.connect('goservice.db')
    cur=con.cursor()
    con.row_factory=sql.Row
    id_profiss=get_id_usuario()
    consulta = '''  SELECT pr.ID_profiss, pr.nome, pr.CPF, pr.telefone, pr.email, pr.endereco, pr.num, pr.bairro, pr.CEP, pr.cidade, pr.uf, pr.profissao
                    FROM profissionais AS pr 
                    WHERE pr.ID_profiss=?'''
    cur.execute(consulta, (id_profiss,))
    profissional = cur.fetchone()
    
    con.close()
    return render_template('/profissional/visual_profissional.html', datas=profissional)

def getUltimoProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf