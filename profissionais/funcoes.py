from flask import  render_template, request, redirect, url_for, flash, jsonify
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user

from app import User_profiss


def verificacao(username, senha):
    con = sql.connect('goservice.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM loginProf WHERE username=?", (username,))
    user_prof = cur.fetchone()
    
    if user_prof and check_password_hash(user_prof[2], senha):
        usuario = User_profiss(username)
        login_user(usuario) #registra o usuário logado, cria uma sessão para o usuário
        return redirect(url_for('prof.protected'))
    flash('Credenciais inválidas', 'error')
    return redirect(url_for('prof.login_profissional'))
    #return render_template('login_profissional.html')


def get_id_usuario():
    con = sql.connect('goservice.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM loginProf WHERE username=?", (current_user.id,))
    id_profiss = cur.fetchone()
    return id_profiss[0]
    con.close()


def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ

def getUltimoProfis():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_profiss) FROM profissionais;")
    id = cur.fetchone()
    idProf=id[0]
    con.close()
    return idProf

def getUltimoServico():
    con = sql.connect("goservice.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(ID_servico) FROM servicos;")
    id = cur.fetchone()
    idServ=id[0]
    con.close()
    return idServ