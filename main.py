from src.app import app

HOST = 'localhost'
PORT = 4000
DEGUB = True

if __name__ == '__main__':
    app.run(HOST, PORT, DEGUB)
    