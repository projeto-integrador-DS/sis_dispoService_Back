import pymysql

# Abrindo uma conexão com o banco de dados
def conecta():
    global con
    con = pymysql.connect (
        host='localhost',
        user='root',
        database='goservice',
        passwd='',
        cursorclass=pymysql.cursors.DictCursor
    )
