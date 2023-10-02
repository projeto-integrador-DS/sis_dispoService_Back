from flask.views import MethodView
from flask import request, render_template, redirect
from src.db import con


class IndexClientes(MethodView):
    def get(self):
        with con.cursor() as cur:
            cur.execute("SELECT * FROM clientes")
            data = cur.fetchall()
            return render_template('/cadastro.html', data=data)
        