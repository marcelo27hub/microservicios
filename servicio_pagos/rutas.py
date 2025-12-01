from flask import request, jsonify
from db import obtener_conexion

TOKEN_SECRETO = "token_mvp_hielos"

def verificar_token(token):
    return token == TOKEN_SECRETO

def registrar_rutas(app):
    @app.post("/pago")
    def realizar_pago():
        encabezado_authorizacion = request.headers.get("Authorization","")
        if not encabezado_authorizacion.startswith("Bearer ") or not verificar_token(encabezado_authorizacion.split(" ")[1]):
            return jsonify({"error":"token invalido"}),401
        datos = request.json or {}
        monto = int(datos.get("monto_centavos",0))
        metodo = datos.get("metodo","desconocido")
        if monto <=0:
            return jsonify({"error":"monto invalido"}),400
        conexion = obtener_conexion()
        conexion.execute("INSERT INTO pagos(monto_centavos,metodo,estado) VALUES (?,?,?)",(monto,metodo,"completado"))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje":"pago realizado","monto_centavos":monto,"metodo":metodo})
