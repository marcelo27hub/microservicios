from flask import Flask
from db import inicializar_bd
from rutas import registrar_rutas

#creamos la app 
def crear_app():
    inicializar_bd()
    app = Flask(__name__)
    registrar_rutas(app)
    return app

#corremos la app
if __name__ == "__main__":
    crear_app().run(port= 5001, debug=True)