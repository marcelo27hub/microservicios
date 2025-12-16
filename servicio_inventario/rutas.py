from flask import request, jsonify
from db import obtener_conexion

TOKEN_SECRETO = "token_hielos"

def verificar_token(token):
    return token == TOKEN_SECRETO


#para las peticciones en el inventario
def registrar_rutas(app):
    
    @app.get("/inventario/<string:sku>")
    #para consultar el sku 
    def consultar_stock(sku):
        conexion = obtener_conexion()
        fila = conexion.execute("SELECT * FROM inventario WHERE sku=?", (sku,)).fetchone()
        conexion.close()
        #si no hay sku
        if not fila:
            return jsonify({"sku":sku,"disponible":0})
        return jsonify(dict(fila))
    
    
    
    #para reservar productos
    @app.post("/inventario/reservar")
    def reservar_stock():
        encabezado_authorizacion = request.headers.get("Authorization","")
        if not encabezado_authorizacion.startswith("Bearer ") or not verificar_token(encabezado_authorizacion.split(" ")[1]):
            return jsonify({"error":"token invalido"}), 401 
        datos = request.json or {}
        sku = datos.get("sku")
        cantidad = int(datos.get("cantidad",0))
        if not sku or cantidad <= 0:
            return jsonify({"error":"datos invalidos"}),400 
        conexion = obtener_conexion()
        fila = conexion.execute("SELECT disponible FROM inventario WHERE sku=?", (sku,)).fetchone()
        if not fila or fila["disponible"]<cantidad:
            conexion.close()
            return jsonify({"error":"stock insuficiente"}),409 
        conexion.execute("UPDATE inventario SET disponible=disponible-? WHERE sku=?",(cantidad,sku))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje":"reservado","sku":sku,"cantidad":cantidad})
    #para liberar stock/ para tener mas 
    @app.post("/inventario/liberar")
    def liberar_stock():
        encabezado_authorizacion = request.headers.get("Authorization","")
        if not encabezado_authorizacion.startswith("Bearer ") or not verificar_token(encabezado_authorizacion.split(" ")[1]):
            return jsonify({"error":"token invalido"}), 401
        datos = request.json or {}
        sku = datos.get("sku")
        cantidad = int(datos.get("cantidad",0))
        if not sku or cantidad <= 0:
            return jsonify({"error":"datos invalidos"}),400 
        conexion = obtener_conexion()
        fila = conexion.execute("SELECT disponible FROM inventario WHERE sku=?", (sku,)).fetchone()
        if not fila:
            conexion.execute("INSERT INTO inventario(sku,disponible) VALUES (?,?)",(sku,cantidad))
        else:
            conexion.execute("UPDATE inventario SET disponible=disponible+? WHERE sku=?",(cantidad,sku))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje":"liberado","sku":sku,"cantidad":cantidad})