import requests

TOKEN = "token_mvp_hielos"

URL_PRODUCTOS = "http://127.0.0.1:5001/productos"
URL_INVENTARIO = "http://127.0.0.1:5002/inventario"
URL_PAGO = "http://127.0.0.1:5003/pago"

def mostrar_productos():
    respuesta = requests.get(URL_PRODUCTOS)
    for p in respuesta.json():
        print(f"{p['sku']}: {p['nombre']} - ${p['precio_centavos']/100:.2f}")

def consultar_stock():
    sku = input("SKU del producto: ")
    respuesta = requests.get(f"{URL_INVENTARIO}/{sku}")
    print(f"Stock disponible: {respuesta.json().get('disponible',0)}")

def reservar_hielo():
    sku = input("SKU del producto: ")
    cantidad = int(input("Cantidad: "))
    respuesta = requests.post(f"{URL_INVENTARIO}/reservar",
                      headers={"Authorization":f"Bearer {TOKEN}"},
                      json={"sku":sku,"cantidad":cantidad})
    print(respuesta.json())

def liberar_hielo():
    sku = input("SKU del producto: ")
    cantidad = int(input("Cantidad: "))
    respuesta = requests.post(f"{URL_INVENTARIO}/liberar",
                      headers={"Authorization":f"Bearer {TOKEN}"},
                      json={"sku":sku,"cantidad":cantidad})
    print(respuesta.json())

def pagar():
    monto = int(input("Monto en centavos: "))
    metodo = input("Método de pago: ")
    respuesta = requests.post(f"{URL_PAGO}",
                      headers={"Authorization":f"Bearer {TOKEN}"},
                      json={"monto_centavos":monto,"metodo":metodo})
    print(respuesta.json())

def menu():
    while True:
        print("\nTienda de Hielos")
        print("1) Listar productos")
        print("2) Consultar stock")
        print("3) Reservar hielo")
        print("4) Liberar hielo")
        print("5) Pagar")
        print("6) Salir")
        opcion = input("Opción: ")
        if opcion=="1": mostrar_productos()
        elif opcion=="2": consultar_stock()
        elif opcion=="3": reservar_hielo()
        elif opcion=="4": liberar_hielo()
        elif opcion=="5": pagar()
        elif opcion=="6": break
        else: print("Opción inválida")

if __name__=="__main__":
    menu()
