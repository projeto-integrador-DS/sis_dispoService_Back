from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from form_db import cur


app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    con = sql.connect("clientes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template('index.html', datas=data)

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        rua = request.form['rua']
        cidade = request.form['cidade']
        numero = request.form['numero']
        estado = request.form['estado']
        email = request.form['email']

        con = sql.connect("clientes.db")
        cur = con.cursor()
        cur.execute("insert into users(NOME,IDADE,RUA,CIDADE,NUMERO,ESTADO,EMAIL) values(?,?,?,?,?,?,?)", (nome, idade, rua, cidade, numero, estado, email))
        con.commit()
        flash('Dados Cadastrados', 'success')
        return redirect(url_for('index'))
    return render_template('add_user.html')


@app.route('/edit_user/<string:id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        rua = request.form['rua']
        cidade = request.form['cidade']
        numero = request.form['numero']
        estado = request.form['estado']
        email = request.form['email']
        
        con = sql.connect("clientes.db")
        cur = con.cursor()
        cur.execute("update users set NOME=?, IDADE=?, RUA=?, CIDADE=?, NUMERO=?, ESTADO=?, EMAIL=?where ID=?", (nome, idade, rua, cidade, numero, estado, email, id))
        con.commit()
        flash('Dados atualizados', 'success')
        return redirect(url_for('index'))
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
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key='marc123'
    app.run(debug=True)
    