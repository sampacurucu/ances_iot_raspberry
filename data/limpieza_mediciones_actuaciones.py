import sqlite3
from datetime import datetime, timedelta
#from data.limpieza_mediciones_actuaciones import eliminar_mediciones_antiguas, eliminar_actuaciones_antiguas
# Función para conectar a la base de datos
def conectar_db():
    db_path = "/home/juanrt88/AncestIoT/data/AncesIoTLocalDatabase.db"
    conn = sqlite3.connect(db_path)
    return conn

# Función para eliminar mediciones sincronizadas y mayores a 10 días
def eliminar_mediciones_antiguas():
    fecha_limite = datetime.now() - timedelta(days=10)
    fecha_limite_str = fecha_limite.strftime('%Y-%m-%d %H:%M:%S')

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Measurement
        WHERE verification = 1 AND timestamp < ?
    """, (fecha_limite_str,))

    conn.commit()
    conn.close()

    print(f"Mediciones eliminadas hasta: {fecha_limite_str}")

# Función para eliminar actuaciones sincronizadas y mayores a 10 días
def eliminar_actuaciones_antiguas():
    fecha_limite = datetime.now() - timedelta(days=10)
    fecha_limite_str = fecha_limite.strftime('%Y-%m-%d %H:%M:%S')

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Actuation
        WHERE verification = 1 AND timestamp < ?
    """, (fecha_limite_str,))

    conn.commit()
    conn.close()

    print(f"Actuaciones eliminadas hasta: {fecha_limite_str}")

# Ejecutar ambas funciones
if __name__ == "__main__":
    eliminar_mediciones_antiguas()
    eliminar_actuaciones_antiguas()