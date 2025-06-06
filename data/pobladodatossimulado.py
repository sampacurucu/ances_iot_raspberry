# pobladodatossimulado.py
import sqlite3
import os
import random
from datetime import datetime, timedelta

def poblar_datos():
    db_path = '/home/juanrt88/AncestIoT/data/AncesIoTLocalDatabase.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener IDs generados
    cursor.execute("SELECT idLocalDevice FROM LocalDevice")
    device_ids = [row[0] for row in cursor.fetchall()]


    # Obtener IDs de sensores y actuadores
    cursor.execute("SELECT idSensor FROM LocalSensor")
    sensor_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT idActuator FROM LocalActuator")
    actuator_ids = [row[0] for row in cursor.fetchall()]

    # 4. Insertar mediciones para sensores
    for sensor_id in sensor_ids:
        for i in range(5):  # 5 mediciones por sensor
            value = round(random.uniform(20, 35), 2)
            timestamp = (datetime.now() - timedelta(minutes=5 * i)).isoformat()
            verification = random.choice([0, 1])
            cursor.execute('''
                INSERT INTO Measurement (idSensor, value, timestamp, verification)
                VALUES (?, ?, ?, ?)
            ''', (sensor_id, value, timestamp, verification))

    conn.commit()
    conn.close()
    print("Datos simulados insertados correctamente.")

if __name__ == "__main__":
    poblar_datos()

