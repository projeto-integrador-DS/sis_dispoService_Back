from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from profissional import getUltimoProfis, get_id_usuario

bp_curso = Blueprint('curso', __name__)


@bp_curso.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    if request.method=='POST':
        modalidade  = request.form['modalidade']
        instituicao = request.form['instituicao']     
        area        = request.form['area']
        fk_idProf = getUltimoProfis()
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (fk_idProf,modalidade, instituicao, area))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return render_template('cad_experiencias.html', cadastro=True)
    return None
    #return render_template('cad_cursos.html', cadastro =True)

@bp_curso.route('/listacursos/')
def list_cursos_prof():
    id_profiss= get_id_usuario()
    print("função list_cursos_prof", id_profiss)
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (id_profiss,))
    cursos = cur.fetchall()      
    return render_template('lista_cursos.html', curs=cursos)

@bp_curso.route('/incluir_curso', methods=['POST', 'GET'])
def incluir_curso():
    id_profiss =get_id_usuario()
    print("chegou no incluir_curso:", id_profiss)
    if request.method=='POST':
        modalidade  = request.form['modalidade']
        instituicao = request.form['instituicao']     
        area        = request.form['area']
        con =  sql.connect('goservice.db')
        cur=con.cursor()
        
        cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (id_profiss,modalidade, instituicao, area))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('curso.list_cursos_prof'))
    return render_template('cad_cursos.html', cadastro = False, id_profiss=id_profiss)
    
@bp_curso.route("/edit_curso/<id_curso>", methods=["POST", "GET"])
def edit_curso(id_curso):
    
    if request.method == 'POST':
        modalidade =    request.form['modalidade']
        instituicao =   request.form["instituicao"]
        area =          request.form["area"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE cursos SET modalidade=?, instituicao=?, area=? WHERE ID_curso=?", (modalidade, instituicao, area, id_curso))
        con.commit()
        flash('Dados atualizados', 'success')
        #id_profiss = get_id_usuario()
        return redirect(url_for('curso.list_cursos_prof'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE c.ID_curso =?", (id_curso,)) 
    #cur.execute("SELECT * FROM cursos WHERE ID_curso=?", (idCurso,))
    curso = cur.fetchone()
    return render_template('edit_cursos.html', cursos=curso)

@bp_curso.route('/delete_curso/<int:id_curso>', methods=['GET'])
def delete_curso(id_curso):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE ID_curso=?", (id_curso,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('curso.list_cursos_prof'))