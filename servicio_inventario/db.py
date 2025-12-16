import sqlite3
from pathlib import Path


BD = Path(__file__).parent / "inventario.db"

def obtener_conexion():
    conexion = sqlite3.connect(BD)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    conexion = obtener_conexion()
    conexion.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        sku TEXT PRIMARY KEY,
        disponible INTEGER NOT NULL
    )
    """)
    inventario_inicial = [
        ("hielo-cub-pequenho",50),
        ("hielo-cub-grande",30),
        ("hielo-triturado",40)
    ]
    for sku,cantidad in inventario_inicial:
        cur = conexion.execute("SELECT * FROM inventario WHERE sku=?",(sku,))
        if not cur.fetchone():
            conexion.execute("INSERT INTO inventario (sku,disponible) VALUES (?,?)",(sku,cantidad))
    conexion.commit()
    conexion.close()