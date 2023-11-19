from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from profissional import getUltimoProfis, get_id_usuario

bp_experiencia=Blueprint('experiencia',__name__)


@bp_experiencia.route('/experiencia', methods=['POST', 'GET'])
def cad_experiencia():
    if request.method == 'POST':
        cargo       = request.form['cargo']
        temp_servico = request.form['temp_servico']
        empresa     = request.form['empresa']

        fk_idProf   = getUltimoProfis()

        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO experiencias(fk_IDprofiss, cargo, temp_servico, empresa) values(?,?,?,?)", (fk_idProf,cargo, temp_servico, empresa))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return render_template('cad_servicos.html',cadastro=True)
        #return redirect(url_for('cad_servicos'))
    return None
    #return render_template('cad_experiencias.html', cadastro=True)

@bp_experiencia.route('/lista_experiencias')
def lista_experiencias():
    id_profiss=get_id_usuario()
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT ID_experiencia, exp.cargo, exp.temp_servico, exp.empresa FROM experiencias AS exp JOIN profissionais AS pr ON pr.ID_profiss = exp.fk_IDprofiss WHERE pr.ID_profiss =?", (id_profiss,))
    experiencias = cur.fetchall()
    return render_template('lista_experiencias.html', exper=experiencias, id_profiss=id_profiss)

@bp_experiencia.route('/add_exper', methods=['POST', 'GET'])
def add_experiencia():
    id_profiss=get_id_usuario()
    if(request.method == 'POST'):
        cargo       = request.form['cargo']
        temp_servico = request.form['temp_servico']
        empresa     = request.form['empresa']
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO experiencias(fk_IDprofiss, cargo, temp_servico, empresa) values(?,?,?,?)", (id_profiss,cargo, temp_servico, empresa))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        
        return redirect(url_for('experiencia.lista_experiencias'))
    return render_template('cad_experiencias.html', cadastro=False)
   
@bp_experiencia.route('/edit_experiencias/<int:idExperiencia>', methods=["POST", "GET"])
def edit_experiencias(idExperiencia):
    
    if request.method == 'POST':
        cargo =      request.form['cargo']
        tempoServico =       request.form["temp_servico"]
        empresa =  request.form["empresa"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE experiencias SET cargo=?, temp_servico=?, empresa=? WHERE ID_experiencia=?", (cargo, tempoServico, empresa, idExperiencia))
        con.commit()
        flash('Dados atualizados', 'success')
        id_profiss=get_id_usuario()
        return redirect(url_for('experiencia.lista_experiencias', id_profiss=id_profiss))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    experiencia = cur.fetchone()
    return render_template('edit_experiencias.html', exper=experiencia)

@bp_experiencia.route('/delete_experiencia/<int:idExperiencia>', methods=['GET'])
def delete_experiencia(idExperiencia):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    con.commit()
    con.close()
    flash('Dados deletados', 'warning')
    id_profiss=get_id_usuario()
    return redirect(url_for('experiencia.lista_experiencias', id_profiss=id_profiss))