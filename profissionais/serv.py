from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
import sqlite3 as sql



serv_blueprint = Blueprint('serv', __name__, template_folder='templates')


#============SERVIÇOS==============
@serv_blueprint.route('/cad_servicos', methods=['POST', 'GET'])
def cad_servicos():
    from profissionais.prof import prof_serv
    from profissionais.funcoes import getUltimoProfis
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
        return redirect(url_for('prof.index'))
    return render_template('cad_Servicos.html')


@serv_blueprint.route('/listaservicos/<int:id_profiss>', methods=['POST', 'GET'])
def lista_servicos():
    from profissionais.funcoes import get_id_usuario
    id_profiss=get_id_usuario()
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row
   
    cur.execute(" SELECT serv.ID_servico, serv.nome, serv.categoria, serv.valor FROM oferece AS o JOIN profissionais AS pr on o.fk_profiss=pr.ID_profiss JOIN servicos AS serv ON o.fk_servic = serv.ID_servico WHERE o.fk_profiss=?", (id_profiss,))
    servicos=cur.fetchall()
    con.close()
    return render_template('lista_servicos.html', serv=servicos)


@serv_blueprint.route('/add_servicos/<int:id_profiss>', methods=['POST', 'GET'])
def add_servicos():
    from profissionais.prof import prof_serv
    from profissionais.funcoes import get_id_usuario
    id_profiss=get_id_usuario()
    if request.method=='POST': 
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']
       
        prof_serv(id_profiss)
        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?, ?)",(nome, categoria, valor))
        con.commit()
        
         #relaciona as tabelas servicos e profissionais

        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('serv.lista_servicos'))
    return render_template('cad_servicos.html', cadastro=False)


@serv_blueprint.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
def edit_servicos(idServico):
    from profissionais.funcoes import  get_id_usuario
    if request.method=='POST':
        nome=request.form['nome']
        categoria=request.form['categoria']
        valor=request.form['valor']

        con = sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("UPDATE servicos SET nome=?, categoria=?, valor=? WHERE ID_servico=?",(nome, categoria, valor, idServico))
        con.commit()
        id_profiss=get_id_usuario()
        return redirect(url_for('serv.lista_servicos', id_profiss=id_profiss))
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row

    cur.execute("SELECT * FROM servicos WHERE ID_servico=?", (idServico,))
    servico =cur.fetchone()
    return render_template('edit_servicos.html', serv=servico)


#---------- Rota Excluir Serviços ----------
@serv_blueprint.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    from profissionais.funcoes import get_id_usuario
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    id_profiss=get_id_usuario()
    return redirect(url_for('lista_servicos', id_profiss=id_profiss))