from flask import Flask
from src.routes.routes import *

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return f"Página não encontrada {e}"

app.add_url_rule(routes["index_route"], view_func=routes["indexclientes"])

