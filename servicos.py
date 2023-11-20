from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from profissional import getUltimoProfis, get_id_usuario

bp_servicos = Blueprint('servico', __name__)

@bp_servicos.route('/cad_servicos', methods=['POST', 'GET'])
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
        return render_template('/profissional/login_profissional.html')
        #return redirect(url_for('login_profissional'))
    return None
    #return render_template('cad_servicos.html', cadastro=True)

@bp_servicos.route('/listaservicos', methods=['POST', 'GET'])
def lista_servicos():
    id_profiss=get_id_usuario()
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row
   
    cur.execute(" SELECT serv.ID_servico, serv.nome, serv.categoria, serv.valor FROM oferece AS o JOIN profissionais AS pr on o.fk_profiss=pr.ID_profiss JOIN servicos AS serv ON o.fk_servic = serv.ID_servico WHERE o.fk_profiss=?", (id_profiss,))
    servicos=cur.fetchall()
    con.close()
    return render_template('/servico/lista_servicos.html', serv=servicos)

@bp_servicos.route('/add_servicos', methods=['POST', 'GET'])
def add_servicos():
    id_profiss=get_id_usuario()
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
        return redirect(url_for('servico.lista_servicos'))
    return render_template('/servico/cad_servicos.html', cadastro=False)

@bp_servicos.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
def edit_servicos(idServico):
    if request.method=='POST':
        nome=request.form['nome']
        categoria=request.form['categoria']
        valor=request.form['valor']

        con = sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("UPDATE servicos SET nome=?, categoria=?, valor=? WHERE ID_servico=?",(nome, categoria, valor, idServico))
        con.commit()
        id_profiss=get_id_usuario()
        return redirect(url_for('servico.lista_servicos', id_profiss=id_profiss))
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row

    cur.execute("SELECT * FROM servicos WHERE ID_servico=?", (idServico,))
    servico =cur.fetchone()
    return render_template('/servico/edit_servicos.html', serv=servico)


@bp_servicos.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    id_profiss=get_id_usuario()
    return redirect(url_for('servico.lista_servicos', id_profiss=id_profiss))

def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

def prof_serv(id_profiss):
    
    id_prof=id_profiss
    #temos um func1 e func2 se o func2 salvar um serviço antes do func1 o func1 terá salvo um serviço do func2
    id_Serv=getUltimoServico()

    con=sql.connect('goservice.db')
    cur=con.cursor()
    
    cur.execute("INSERT INTO oferece (fk_profiss, fk_servic) values(?,?)", (id_prof, id_Serv))
    con.commit()
    con.close()