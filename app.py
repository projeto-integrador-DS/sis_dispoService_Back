from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql


app = Flask(__name__)

@app.route('/')
def inicial():
    return render_template('inicial_01.html')

@app.route('/login_cliente')
def loginCliente():
    return render_template('login.html')


@app.route('/menu_cliente')
def menu_cliente():
    return render_template('menu_cliente.html')


@app.route('/clientes_cadastrados')
def clientes_cadastrados():
    con = sql.connect("clientes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template('cadastrados.html', datas=data)

@app.route('/cadastre-se', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        rua = request.form['rua']
        numero = request.form['numero']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        cep = request.form['cep']
        foto = request.form['foto']

        con = sql.connect("clientes.db")
        cur = con.cursor()
        cur.execute("insert into users(NOME, EMAIL, CPF, TELEFONE, RUA, NUMERO, BAIRRO, CIDADE, ESTADO, CEP, FOTO) values (?,?,?,?,?,?,?,?,?,?,?)", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, foto))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('inicial'))
    return render_template('add_user.html')


@app.route('/edit_user/<string:id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        rua = request.form['rua']
        numero = request.form['numero']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        cep = request.form['cep']
        foto = request.form['foto']
        
        con = sql.connect("clientes.db")
        cur = con.cursor()
        cur.execute("update users set NOME=?, EMAIL=?, CPF=?, TELEFONE=?, RUA=?, NUMERO=?, CIDADE=?, BAIRRO=?, ESTADO=?, CEP=?, FOTO=? where ID=?", (nome, email, cpf, telefone, rua, numero, cidade, bairro, estado, cep, foto, id))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('inicial'))
    con = sql.connect("clientes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where ID=?", (id))
    data = cur.fetchone()
    return render_template('edit_user.html', datas=data)


@app.route('/delete_user/<string:id>', methods=['GET'])
def delete_user(id):
    con = sql.connect("clientes.db")
    cur = con.cursor()
    cur.execute("delete from users where ID=?", (id))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('inicial'))

if __name__ == '__main__':
    app.secret_key='marc123'
    app.run(debug=True)
    
from form_db import cur

app = Flask(__name__)
app.secret_key="daniel123"


#@app.route('/')
@app.route('/index')
def index():
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM profissionais AS pr  JOIN cursos AS cur ON pr.ID_profiss = cur.fk_idProfiss JOIN experiencias AS exp ON pr.ID_profiss = exp.fk_IDprofiss;")
    data = cur.fetchall()       
    return render_template('index.html', datas=data)

@app.route('/')
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
        return render_template('cad_cursos.html') 
 
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
    print(type(fk_idProf))
    con =  sql.connect('goservice.db')
    cur=con.cursor()
    cur.execute("INSERT INTO cursos(fk_idProfiss, modalidade, instituicao, area) values (?,?,?,?)", (fk_idProf,modalidade, instituicao, area))
    con.commit()
    flash('Dados Cadastrados', 'success')
    con.close()
    return render_template('cad_experiencias.html')

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
    return redirect(url_for('index'))


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
        print("executando a função cadServicos")
        nome    =   request.form['nome']
        categoria=  request.form['categoria']
        valor   =   request.form['valor']
    
        con=sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO servicos(nome, categoria, valor) values(?, ?, ?)",(nome, categoria, valor))
        con.commit()
        flash('Dados Cadastrados', 'success')
        con.close()
        return redirect(url_for('indexServico'))
        
    return render_template('cad_Servicos.html')
    
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

if __name__ == '__main__':
    app.run(debug=True)
