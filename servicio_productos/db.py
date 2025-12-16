import sqlite3
from pathlib import Path

#creamos nuestra base de datos
BD = Path(__file__).parent / "productos.db"

#obtenemos la conexion 
def obtener_conexion():
    conexion = sqlite3.connect(BD)
    conexion.row_factory = sqlite3.Row
    return conexion

#inicialisamos nuestra base de datos
def inicializar_bd():
    conexion =obtener_conexion()
    conexion.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        precio_centavos INTEGER NOT NULL)
        """)
    #productos disponibles
    productos = [
        ("hielo-cub-pequenho", "cubitos pequenho", 500),
        ("hielo-cub-grande", "cubitos grande", 800),
        ("hielo-cub-triturado", "hielo triturado", 600)
    ]
    
    #revisamos si el sku ya esta o no
    for sku, nombre, precio in productos:
        cursor = conexion.execute("SELECT * FROM productos WHERE sku = ?",
                                  (sku,))
        if not cursor.fetchone():
            conexion.execute("INSERT INTO productos(sku, nombre, precio_centavos) VALUES (?,?,?)",
                             (sku,nombre,precio))

    conexion.commit()
    conexion.close()