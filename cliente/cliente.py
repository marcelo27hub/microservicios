import time
import requests

TOKEN = "token_hielos"

URL_PRODUCTOS = "http://127.0.0.1:5001/productos"
URL_INVENTARIO = "http://127.0.0.1:5002/inventario"
URL_PAGO = "http://127.0.0.1:5003/pago"

# circuit breaker

MAXIMO_FALLOS = 3        
TIEMPO_BLOQUEADO = 5     

fallos_seguidos = 0
bloqueado_hasta = 0


def solicitud_segura(metodo, url, **argumentos):
    """
    Envuelve requests con Circuit Breaker.
    metodo = "GET" o "POST"
    """
    global fallos_seguidos, bloqueado_hasta

    # Si está bloqueado, no intenta pedir
    if time.time() < bloqueado_hasta:
        print(" Servicio temporalmente bloqueado. Intente más tarde...")
        return None
    
    # Intento normal + 1 retry
    for intento in range(2):
        try:
            print(f"[LOG] Intento {intento+1} → {metodo} {url}")  # log mínimo
            respuesta = requests.request(metodo, url, timeout=2, **argumentos)

            if respuesta.ok:
                fallos_seguidos = 0
                return respuesta

            fallos_seguidos += 1
            print(f"[LOG] Respuesta no válida. Código: {respuesta.status_code}")

        except Exception as e:
            fallos_seguidos += 1
            print(f"[LOG] Error intento {intento+1}: {e}")

    if fallos_seguidos >= MAXIMO_FALLOS:
        bloqueado_hasta = time.time() + TIEMPO_BLOQUEADO
        print("CORTACIRCUITO ACTIVADO — demasiados fallos consecutivos!")

    return None


# FUNCIONES DEL CLIENTE

def mostrar_productos():
    respuesta = solicitud_segura("GET", URL_PRODUCTOS)
    
    if not respuesta:
        print(" No se pudieron obtener los productos.")
        return
    
    print("\n LISTA DE PRODUCTOS\n")
    for p in respuesta.json():
        print(f"SKU {p['sku']} — {p['nombre']} — ${p['precio_centavos']/100:.2f}")


def consultar_stock():
    sku = input("\nIngrese SKU del producto: ")
    respuesta = solicitud_segura("GET", f"{URL_INVENTARIO}/{sku}")

    if not respuesta:
        print(" No se pudo consultar el inventario.")
        return
    
    print(f" Stock disponible: {respuesta.json().get('disponible',0)}")


def reservar_producto():
    sku = input("\nSKU del producto a reservar: ")
    cantidad = int(input("Cantidad: "))

    respuesta = solicitud_segura(
        "POST",
        f"{URL_INVENTARIO}/reservar",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"sku": sku, "cantidad": cantidad}
    )
    print(respuesta.json() if respuesta else " No se pudo reservar el producto.")


def liberar_producto():
    sku = input("\nSKU del producto a liberar: ")
    cantidad = int(input("Cantidad: "))

    respuesta = solicitud_segura(
        "POST",
        f"{URL_INVENTARIO}/liberar",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"sku": sku, "cantidad": cantidad}
    )
    print(respuesta.json() if respuesta else " No se pudo liberar.")


def realizar_pago():
    monto = int(input("\nMonto en centavos: "))
    metodo = input("Método de pago (tarjeta/efectivo/etc): ")
    sku = input("SKU del producto: ")
    cantidad = int(input("Cantidad: "))

    respuesta = solicitud_segura(
        "POST",
        URL_PAGO,
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={
            "monto_centavos": monto,
            "metodo": metodo,
            "sku": sku,
            "cantidad": cantidad
        }
    )

    print(respuesta.json() if respuesta else " No se pudo procesar el pago.")

        

# MENÚ DEL CLIENTE

def menu():
    while True:
        print("\n🧊 TIENDA DE HIELOS")
        print("1) Mostrar productos")
        print("2) Consultar stock")
        print("3) Reservar producto")
        print("4) Liberar producto reservado")
        print("5) Realizar pago")
        print("6) Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": 
            mostrar_productos()
        elif opcion == "2": 
            consultar_stock()
        elif opcion == "3": 
            reservar_producto()
        elif opcion == "4": 
            liberar_producto()
        elif opcion == "5": 
            realizar_pago()
        elif opcion == "6":
            print("¡Gracias por comprar con nosotros!")
            break
        else:
            print(" Opción inválida")


if __name__ == "__main__":
    menu()