import sqlite3
from pathlib import Path #para manejar rutas path

#creo mi base de datos
BD = Path(__file__).parent / "pagos.db"

def obtener_conexion():
    conexion = sqlite3.connect(BD)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    conexion = obtener_conexion()
    conexion.execute("""
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monto_centavos INTEGER NOT NULL,
        metodo TEXT NOT NULL,
        estado TEXT NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()