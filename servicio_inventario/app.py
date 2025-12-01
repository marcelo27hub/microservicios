from flask import Flask
from db import inicializar_db
from rutas import registrar_rutas


def crear_app():
    inicializar_db()
    app = Flask(__name__)
    registrar_rutas(app)
    return app

if __name__=="__main__":
    crear_app().run(port=5002, debug=True)