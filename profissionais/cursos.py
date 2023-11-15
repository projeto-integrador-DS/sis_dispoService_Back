from flask import  render_template, request, redirect, url_for, flash, Blueprint
import sqlite3 as sql



cursos_blueprint = Blueprint('exp', __name__, template_folder='templates')


#============CURSOS==============
@cursos_blueprint.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    from profissionais.funcoes import getUltimoProfis
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
        return redirect(url_for('expe.cad_experiencia'))
    return render_template('cad_cursos.html', cadastro =True)



@cursos_blueprint.route('/listacursos/<int:id_profiss>')
def list_cursos_prof():
    from profissionais.funcoes import get_id_usuario
    id_profiss= get_id_usuario()
    print("função list_cursos_prof", id_profiss)
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (id_profiss,))
    cursos = cur.fetchall()      
    return render_template('lista_cursos.html', curs=cursos)


@cursos_blueprint.route('/incluir_curso', methods=['POST', 'GET'])
def incluir_curso():
    from profissionais.funcoes import get_id_usuario
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
        return redirect(url_for('list_cursos_prof'))
    return render_template('cad_cursos.html', cadastro = False, id_profiss=id_profiss)


@cursos_blueprint.route("/edit_curso/<int:idCurso>", methods=["POST", "GET"])
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
        return redirect(url_for('cursos.list_cursos_prof'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE c.ID_curso =?", (id_curso,)) 
    curso = cur.fetchone()
    return render_template('edit_cursos.html', cursos=curso)



@cursos_blueprint.route('/delete_curso/<int:idCurso>', methods=['GET'])
def delete_curso(id_curso):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE ID_curso=?", (id_curso,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('cursos.list_cursos_prof'))