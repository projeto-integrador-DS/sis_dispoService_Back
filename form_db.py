import sqlite3 as sql

con = sql.connect('clientes.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users')


sql = '''CREATE TABLE "users"(
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "IDADE" TEXT,
    "RUA" TEXT,
    "CIDADE" TEXT,
    "NUMERO" TEXT,
    "ESTADO" TEXT,
    "EMAIL" TEXT
    )'''

cur.execute(sql)
con.commit()
con.close()
