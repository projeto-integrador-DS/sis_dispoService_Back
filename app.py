from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from form_db import cur

app = Flask(__name__)
app.secret_key="daniel123"

@app.route('/')
@app.route('/index')
def index():
    #cur.execute("SELECT * FROM profissionais AS pr  JOIN cursos AS cur ON pr.ID_profiss = cur.fk_idProfiss JOIN experiencias AS exp ON pr.ID_profiss = exp.fk_IDprofiss;")
               
    return render_template('index.html')


@app.route('/indexServico')
def indexServico():
    con=sql.connect("goservice.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM servicos")
    servico=cur.fetchall()

    return render_template('indexServicos.html', servicos=servico)

#============PROFISSIONAIS==============
@app.route('/cad_profissionais', methods=['POST', 'GET'])
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
        return render_template('cad_cursos.html', cadastro=True) 
 
    return render_template('cad_profissionais.html')


@app.route('/edit_profissionais/<int:idProf>', methods=['POST', 'GET'])
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

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE profissionais SET nome=?, cpf=?, telefone=?, email=?, endereco=?, cidade=?, num=?, bairro=?, cep=?, uf=? WHERE ID_profiss=?", (nome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, idProf))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('index'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (idProf,))
    data = cur.fetchone()
    return render_template('edit_profissionais.html', datas=data)

@app.route('/delete_profissionais/<int:idProf>', methods=['GET'])
def delete_profissionais(idProf):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID_profiss=?", (idProf,))
    con.commit()
    flash('Dados deletados', 'warning')
    
    return redirect(url_for('index'))

#============CURSOS==============
@app.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    
    modalidade  = request.form['modalidade']
    instituicao = request.form['instituicao']     
    area        = request.form['area']
    fk_idProf = findIDProfis()
    
    con =  sql.connect('goservice.db')
    cur=con.cursor()
    cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (fk_idProf,modalidade, instituicao, area))
    con.commit()
    flash('Dados Cadastrados', 'success')
    con.close()
    return render_template('cad_experiencias.html', cadastro=True)

@app.route('/listacursos/<int:id_profiss>')
def list_cursos_prof(id_profiss):
    
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.ID_curso, c.modalidade, c.instituicao, c.area FROM cursos AS c JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss WHERE pr.ID_profiss =?", (id_profiss,))
    cursos = cur.fetchall()       
    return render_template('lista_cursos.html', curs=cursos)

#deverá ter uma parâmetro: id_profiss
@app.route('/incluir_curso/<id_profiss>', methods=['POST', 'GET'])
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
        return redirect(url_for('list_cursos_prof',id_profiss=1))
    return render_template('cad_cursos.html', cadastro = False)
    

@app.route("/edit_curso/<int:idCurso>", methods=["POST", "GET"])
def edit_curso(idCurso):
    
    if request.method == 'POST':
        modalidade =      request.form['modalidade']
        instituicao =       request.form["instituicao"]
        area =  request.form["area"]

        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE cursos SET modalidade=?, instituicao=?, area=? WHERE ID_curso=?", (modalidade, instituicao, area, idCurso))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('index'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM cursos WHERE ID_curso=?", (idCurso,))
    curso = cur.fetchone()
    return render_template('edit_cursos.html', cursos=curso)

@app.route('/delete_curso/<int:idCurso>', methods=['GET'])
def delete_curso(idCurso):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE ID_curso=?", (idCurso,))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

def findIDProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf

#============EXPERIÊNCIAS==============
@app.route('/experiencia', methods=['POST', 'GET'])
def cad_experiencia():
    cargo       = request.form['cargo']
    temp_servico = request.form['temp_servico']
    empresa     = request.form['empresa']
    fk_idProf   = findIDProfis()
    con =  sql.connect('goservice.db')
    cur=con.cursor()
    cur.execute("INSERT INTO experiencias(fk_IDprofiss, cargo, temp_servico, empresa) values(?,?,?,?)", (fk_idProf,cargo, temp_servico, empresa))
    con.commit()
    flash('Dados Cadastrados', 'success')
    con.close()
    return render_template('cad_servicos.html')

@app.route('/lista_experiencias/<int:id_profiss>')
def lista_experiencias(id_profiss):
    con = sql.connect("goservice.db")
    
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT ID_experiencia, exp.cargo, exp.temp_servico, exp.empresa FROM experiencias AS exp JOIN profissionais AS pr ON pr.ID_profiss = exp.fk_IDprofiss WHERE pr.ID_profiss =?", (id_profiss,))
    experiencias = cur.fetchall()
            
    return render_template('lista_experiencias.html', exper=experiencias)

@app.route('/add_exper/<int:id_profiss>', methods=['POST', 'GET'])
def add_experiencia(id_profiss):
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
        
        return redirect(url_for('lista_experiencias', id_profiss=id_profiss))
    return render_template('cad_experiencias.html', cadastro=False)
   
@app.route('/edit_experiencias/<int:idExperiencia>', methods=["POST", "GET"])
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
        return redirect(url_for('index'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    experiencia = cur.fetchone()
    return render_template('edit_experiencias.html', exper=experiencia)

@app.route('/delete_experiencia/<int:idExperiencia>', methods=['GET'])
def delete_experiencia(idExperiencia):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM experiencias WHERE ID_experiencia=?", (idExperiencia,))
    con.commit()
    con.close()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

#============SERVIÇOS==============
@app.route('/cad_servicos', methods=['POST', 'GET'])
def cad_servicos():
    if request.method=='POST':
        
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']

        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('index'))

    return render_template('cad_servicos.html')

@app.route('/edit_servicos/<int:idServico>', methods=["POST", "GET"])
def edit_servicos(idServico):
    if request.method=='POST':
        nome=request.form['nome']
        categoria=request.form['categoria']
        valor=request.form['valor']

        con = sql.connect('goservice.db')
        cur=con.cursor()
        cur.execute("UPDATE servicos SET nome=?, categoria=?, valor=? WHERE ID_servico=?",(nome, categoria, valor, idServico))
        con.commit()
        return redirect(url_for('indexServico'))
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.row_factory=sql.Row

    cur.execute("SELECT * FROM servicos WHERE ID_servico=?", (idServico,))
    servico =cur.fetchone()
    return render_template('edit_servicos.html', serv=servico)

@app.route('/delete_servicos/<int:idServico>', methods=["GET"])
def delete_servicos(idServico):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("DELETE FROM servicos WHERE ID_servico=?", (idServico,))
    con.commit()
    con.close()
    return render_template('indexServicos.html')

#============RELACIONA SERVIÇO COM PROFISSIONAL==============
def prof_serv():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    id_prof=cur.execute("SELECT ID_profiss FROM profissionais").fetchone()
    id_prof=id_prof[0]

    id_Serv=cur.execute("SELECT ID_servico FROM servicos").fetchone()
    id_Serv=id_Serv[0]
    
    cur.execute("INSERT INTO oferece (fk_profiss, fk_servic) values(?,?)", (id_prof, id_Serv))
    con.commit()
  
    con.close()

prof_serv()

if __name__ == '__main__':
    app.run(debug=True)