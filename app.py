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
    cur.execute("select * from profissionais")
    data = cur.fetchall()
    return render_template('index.html', datas=data)

@app.route('/cad_profissionais', methods=['POST', 'GET'])
def cad_profissionais():
    if request.method == 'POST':
        nome =      request.form['nome']
        sobrenome = request.form["sobrenome"]
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["cep"]
        uf =        request.form['uf']
        complemen = request.form["complemento"]
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("INSERT INTO profissionais(nome, sobrenome, cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, complemen) values(?,?,?,?,?,?,?,?,?,?,?,?)", 
                    (nome, sobrenome,cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, complemen))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('index'))
    return render_template('cad_profissionais.html')


@app.route('/cad_profissionais/<string:id>', methods=['POST', 'GET'])
def edit_profissionais(id):
    if request.method == 'POST':
        nome =      request.form['nome']
        sobrenome = request.form["sobrenome"]
        cpf =       request.form["cpf"]
        telefone =  request.form["telefone"]  
        email =     request.form['email']
        endereco =  request.form['endereco']
        cidade =    request.form['cidade']
        num =       request.form['numero']
        bairro =    request.form["bairro"]
        cep =       request.form["CEP"]
        uf =        request.form['uf']
        complemen = request.form["complemento"]
        
        con = sql.connect("goservice.db")
        cur = con.cursor()
        cur.execute("UPDATE profissionais SET nome=?, sobrenome=?, cpf=?, telefone=?, endereco=?, cidade=?, num=?, bairro=?, cep=?, uf=?, complemen=?, where ID_profiss=?", 
                    (nome, sobrenome,cpf, telefone, email, endereco, cidade, num, bairro, cep, uf, complemen))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('index'))
    con = sql.connect("goservice.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM profissionais WHERE ID_profiss=?", (id))
    data = cur.fetchone()
    return render_template('edit_profissionais.html', datas=data)


@app.route('/delete_profissionais/<string:id>', methods=['GET'])
def delete_profissionais(id):
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("DELETE FROM profissionais WHERE ID=?", (id))
    con.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key='marc123'
    app.run(debug=True)
    