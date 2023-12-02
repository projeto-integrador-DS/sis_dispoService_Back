import sqlite3 as sql
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, UserMixin, login_required, LoginManager
from flask import redirect, render_template, url_for, flash, Blueprint, request


bp_logincli = Blueprint("logincliente",__name__, template_folder='templates')

login_manager_cliente = LoginManager()

