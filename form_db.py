import sqlite3 as sql

con = sql.connect('clientes.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users')


sql = '''CREATE TABLE "users"(
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "EMAIL" TEXT,
    "CPF" TEXT,
    "TELEFONE" TEXT,
    "RUA" TEXT,
    "NUMERO" TEXT,
    "BAIRRO" TEXT,
    "CIDADE" TEXT,
    "ESTADO" TEXT,
    "CEP" TEXT,
    "FOTO" TEXT
    )'''

cur.execute(sql)
con.commit()
con.close()
