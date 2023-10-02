import pymysql.cursors

# Abrindo uma conexão com o banco de dados
con = pymysql.connect (
    host='localhost',
    user='root',
    database='goservice',
    passwd='',
    cursorclass=pymysql.cursors.DictCursor
)
