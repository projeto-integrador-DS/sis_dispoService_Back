from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'O Senhor dos aneis - A sociedade do Anel',
        'autor': 'J.R.R Tolkien' 
    },

    {
        'id': 2,
        'titulo': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J.K Howling' 
    },

    {
        'id': 3,
        'titulo': 'James Clear',
        'autor': 'Hábitos Atômicos' 
    },
]

#Criação de um modelo de API de consulta de livro para fins de aprendizado


#Consultar todos os livros
@app.route('/livros', methods=['GET'])
def obter_livros():
    return jsonify(livros)

#Coonsultar livro por id
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
 
app.run(port=5000, host='localhost', debug=True)