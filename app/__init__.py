from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db' #Usarei o sqlite3 mas em breve usarei o mysql
db = SQLAlchemy(app)

from app.controllers import default



