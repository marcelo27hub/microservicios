from flask import request, jsonify
from db import obtener_conexion

TOKE_SECRETO = "token_hielos"

def verificar_token(token):
    return token == TOKE_SECRETO

def registrar_rutas(app):
    @app.get("/productos")
    def listar_productos():
        conexion = obtener_conexion()
        filas = conexion.execute("SELECT * FROM productos").fetchall()
        conexion.close()
        return jsonify([dict(f) for f in filas])
    @app.post("/productos")
    def crear_productos():
        encabezado_authorizacion = request.headers.get("Authorizacion", "")
        if not encabezado_authorizacion.startswith("bearer ") or not verificar_token(encabezado_authorizacion.split(" ")[1]):
            return jsonify({"error": "token invalido"}), 401
        datos = request.json or {}
        if not all(dato in datos for dato in ("sku", "nombre", "precio_centavos")):
            return jsonify({"error":"faltan campos"}), 400
        conexion = obtener_conexion()
        try:
            conexion.execute("INSERT INTO productos (sku,nombre,precio_centavos) VALUES (?,?,?)",
                             (datos["sku"],datos["nombre"],datos["precio_centavos"]))
            conexion.commit()
            conexion.close()
            return jsonify({"mensaje":"creado"}), 201
        except Exception as e:
            conexion.close()
            return jsonify({"error": str(e)}), 400