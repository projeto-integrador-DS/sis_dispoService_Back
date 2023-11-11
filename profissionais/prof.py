from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_login import LoginManager
import sqlite3 as sql

prof_blueprint = Blueprint('prof', __name__, template_folder='templates')



#---------- Começo CRUD Profissionais ----------

@prof_blueprint.route('/index')
def index(): 
    return render_template('index.html')

@prof_blueprint.route('/indexServico')
def indexServico():
    con=sql.connect("goservice.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM servicos")
    servico=cur.fetchall()

    return render_template('indexServicos.html', servicos=servico)


#============PROFISSIONAIS==============
@prof_blueprint.route('/cad_profissionais', methods=['POST', 'GET'])
def cad_profissionais():
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
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO profissionais(nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf) values(?,?,?,?,?,?,?,?,?,?)", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('clientes.inicial'))
        #return render_template('cad_cursos.html', cadastro=True) 
 
    return render_template('cad_profissionais.html')



#======================Editar Profissionais=======================
@prof_blueprint.route('/edit_profissionais/<int:idProf>', methods=['POST', 'GET'])
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
        cep =       request.form["cep"]
        uf =        request.form['uf']


        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE profissionais SET nome=?, cpf=?, telefone=?, email=?, endereco=?, cidade=?, num=?, bairro=?, cep=?, uf=? WHERE ID_profiss=?", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, idProf))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('inicial'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (idProf,))
    data = cur.fetchone()
    return render_template('edit_profissionais.html', datas=data)


#================Deletar Profissionais==================
@prof_blueprint.route('/delete_profissionais/<int:idProf>', methods=['GET'])
def delete_profissionais(idProf):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID_profiss=?", (idProf,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('index'))



#============CURSOS==============
@prof_blueprint.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    
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



@prof_blueprint.route('/listacursos/<int:id_profiss>')
def list_cursos_prof(id_profiss):
    
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (id_profiss,))
    cursos = cur.fetchall()       
    return render_template('lista_cursos.html', curs=cursos)



@prof_blueprint.route('/incluir_curso/<id_profiss>', methods=['POST', 'GET'])
def incluir_curso(id_profiss):
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
        return redirect(url_for('list_cursos_prof',id_profiss=id_profiss))#id_profiss=id_profiss ainda não testado
    return render_template('cad_cursos.html', cadastro = False)


@prof_blueprint.route("/edit_curso/<int:idCurso>", methods=["POST", "GET"])
def edit_curso(idCurso):
    
    if request.method == 'POST':
        modalidade =    request.form['modalidade']
        instituicao =   request.form["instituicao"]
        area =          request.form["area"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE cursos SET modalidade=?, instituicao=?, area=? WHERE ID_curso=?", (modalidade, instituicao, area, idCurso))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('list_cursos_prof', id_profiss=1))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (idCurso,)) 
    #cur.execute("SELECT * FROM cursos WHERE ID_curso=?", (idCurso,))
    curso = cur.fetchone()
    return render_template('edit_cursos.html', cursos=curso)



@prof_blueprint.route('/delete_curso/<int:idCurso>', methods=['GET'])
def delete_curso(idCurso):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE ID_curso=?", (idCurso,))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('list_cursos_prof', id_profiss=1))


def getUltimoProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf


#============SERVIÇOS==============
@prof_blueprint.route('/cad_servicos', methods=['POST', 'GET'])
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


@prof_blueprint.route('/listaservicos/<int:id_profiss>', methods=['POST', 'GET'])
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


@prof_blueprint.route('/add_servicos/<int:id_profiss>', methods=['POST', 'GET'])
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


@prof_blueprint.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
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
@prof_blueprint.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    return redirect(url_for('lista_servicos', id_profiss=1))

def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

#============RELACIONA SERVIÇO COM PROFISSIONAL==============
def prof_serv(id_profiss):
    
    id_prof=id_profiss
    #temos um func1 e func2 se o func2 salvar um serviço antes do func1 o func1 terá salvo um serviço do func2
    id_Serv=getUltimoServico()

    con=sql.connect('goservice.db')
    cur=con.cursor()
    
    cur.execute("INSERT INTO oferece (fk_profiss, fk_servic) values(?,?)", (id_prof, id_Serv))
    con.commit()
    con.close()