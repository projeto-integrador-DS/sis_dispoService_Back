from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:14@Mmy14@localhost/goservice' 
db = SQLAlchemy(app)

from app.controllers import default



