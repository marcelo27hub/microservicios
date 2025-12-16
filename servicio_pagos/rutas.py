from flask import request, jsonify
from db import obtener_conexion
import requests

TOKEN_SECRETO = "token_hielos"
INVENTARIO_URL = "http://127.0.0.1:5002/inventario" 

def verificar_token(token):
    return token == TOKEN_SECRETO

def registrar_rutas(app):
    #endpoint para procesar el pago y que metodo sera (cash/efectivo/etc)
    @app.post("/pago")
    def realizar_pago():
        encabezado_authorizacion = request.headers.get("Authorization","")
        if not encabezado_authorizacion.startswith("Bearer ") or not verificar_token(encabezado_authorizacion.split(" ")[1]):
            return jsonify({"error":"token invalido"}),401
        datos = request.json or {}
        monto = int(datos.get("monto_centavos",0))
        metodo = datos.get("metodo","desconocido")
        
        sku = datos.get("sku")               
        cantidad = datos.get("cantidad")     
        if monto <=0:
            return jsonify({"error":"monto invalido"}),400
        if not sku or not cantidad:
            return jsonify({"error":"faltan datos: sku y cantidad"}),400
        
        #autenticacion entre inventario y poago 
        respuesta_inventario = requests.get(
            f"{INVENTARIO_URL}/{sku}",
            headers={"Authorization": f"Bearer {TOKEN_SECRETO}"}   #autenticación entre servicios
        )    
        
        #verificamos si hay respuesta valida por parte del servicio de inventario
        if not respuesta_inventario.ok:
            return jsonify({"error":"inventario no disponible"}),503

        stock = respuesta_inventario.json().get("disponible",0)

        if stock < cantidad:
            return jsonify({"error":"stock insuficiente"}),409
        
        reserva = requests.post(
            f"{INVENTARIO_URL}/reservar",
            headers={"Authorization": f"Bearer {TOKEN_SECRETO}"},
            json={"sku": sku, "cantidad": cantidad}
        )

        if not reserva.ok:
            return jsonify({"error":"no se pudo reservar stock"}), 500

        # registrar el pago en la bd
        conexion = obtener_conexion()
        conexion.execute(
            "INSERT INTO pagos(monto_centavos,metodo,estado) VALUES (?,?,?)",
            (monto, metodo, "completado")
        )
        conexion.commit()
        conexion.close()

        return jsonify({
            "mensaje":"pago realizado",
            "monto_centavos":monto,
            "metodo":metodo,
            "stock_reservado":cantidad,
            "sku":sku
        })