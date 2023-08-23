from app import app


@app.route("/")
def index():
    return "<h1>Seja bem vindo a GoService</h1>"
