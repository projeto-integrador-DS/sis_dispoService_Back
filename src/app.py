# objeto da classe flask é o WSGI.
from flask import Flask, redirect, url_for, request
 

app = Flask(__name__)
"""
def teste():
    return "teste-test"
app.add_url_rule("/", "gfg", gfg)
"""

"""
@app.route('/ola/<nome>')
def teste(nome):
    return 'ola %s!' % nome
"""
@app.route('/sucesso/<nome>')
def telaBoasVindas(nome):
    return 'bem vindo %s' % nome

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        profissional = request.form['nm']
        return redirect(url_for('static', nome=profissional))
    else:
        profisional = request.args.get('nm')
        return redirect(url_for('static', nome=profisional))
if __name__ == '__main__':
    app.run()

