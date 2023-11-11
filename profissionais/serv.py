from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_login import LoginManager
import sqlite3 as sql

#---------importando funções do prof.py----------
from profissionais.prof import getUltimoProfis
from profissionais.prof import prof_serv


serv_blueprint = Blueprint('serv', __name__, template_folder='templates')


#============SERVIÇOS==============
@serv_blueprint.route('/cad_servicos', methods=['POST', 'GET'])
def cad_servicos():
    if request.method=='POST':
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']
        
        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        #pega o ultimo id do profissional cadastrado
        ultimIDprof=getUltimoProfis()
        prof_serv(ultimIDprof)
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('index'))
    return render_template('cad_Servicos.html')


@serv_blueprint.route('/listaservicos/<int:id_profiss>', methods=['POST', 'GET'])
def lista_servicos(id_profiss):
    #essa função é chamada 2x (get e post) por isso está cadastrando 2x
     #apenas para fins de teste
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row
    
    cur.execute("SELECT serv.ID_servico, serv.nome, serv.categoria, serv.valor FROM servicos AS serv JOIN profissionais AS pr JOIN oferece AS o ON serv.ID_servico=o.fk_servic WHERE pr.ID_profiss =?", (id_profiss,))
    servicos=cur.fetchall()
    con.close()
    return render_template('lista_servicos.html', serv=servicos)


@serv_blueprint.route('/add_servicos/<int:id_profiss>', methods=['POST', 'GET'])
def add_servicos(id_profiss):
    if request.method=='POST': 
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']

        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        
        prof_serv(id_profiss) #relaciona as tabelas servicos e profissionais

        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('lista_servicos', id_profiss=id_profiss))
    return render_template('cad_Servicos.html', cadastro=False)


@serv_blueprint.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
def edit_servicos(idServico):
    if request.method=='POST':
        nome=request.form['nome']
        categoria=request.form['categoria']
        valor=request.form['valor']

        con = sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("UPDATE servicos SET nome=?, categoria=?, valor=? WHERE ID_servico=?",(nome, categoria, valor, idServico))
        con.commit()
        return redirect(url_for('lista_servicos', id_profiss=1))
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row

    cur.execute("SELECT * FROM servicos WHERE ID_servico=?", (idServico,))
    servico =cur.fetchone()
    return render_template('edit_servicos.html', serv=servico)


#---------- Rota Excluir Serviços ----------
@serv_blueprint.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    return redirect(url_for('lista_servicos', id_profiss=1))