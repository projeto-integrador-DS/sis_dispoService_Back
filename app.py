from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from form_db import cur


app = Flask(__name__)
app.secret_key="daniel123"


@app.route('/')
@app.route('/index')
def index():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    #cur.execute("select * from profissionais")
    cur.execute("SELECT * FROM profissionais AS pr  JOIN cursos AS cur ON pr.ID_profiss = cur.fk_idProfiss JOIN experiencias AS exp ON pr.ID_profiss = exp.fk_IDprofiss;")
    data = cur.fetchall()
    return render_template('index.html', datas=data)

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
        return render_template('cad_cursos.html') 
 
    return render_template('cad_profissionais.html')

@app.route('/curso', methods=['POST', 'GET'])
def cad_curso():
    
    modalidade  = request.form['modalidade']
    instituicao = request.form['instituicao']     
    area        = request.form['area']
    fk_idProf = findIDProfis()
    print(type(fk_idProf))
    con =  sql.connect('goservice.db')
    cur=con.cursor()
    cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (fk_idProf,modalidade, instituicao, area))
    con.commit()
    flash('Dados Cadastrados', 'success')
    con.close()
    return render_template('cad_experiencias.html')

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
    return redirect(url_for('index'))

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

def findIDProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf

if __name__ == '__main__':
    app.secret_key='marc123'
    app.run(debug=True)
    