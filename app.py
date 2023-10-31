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
    