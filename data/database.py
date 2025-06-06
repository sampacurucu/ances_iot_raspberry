# crear_tablas.py
import sqlite3
import os

def crear_tablas():
    db_path = os.path.join('data', 'AncesIoTLocalDatabase.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla LocalDevice
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LocalDevice (
            idLocalDevice INTEGER PRIMARY KEY,
            idGateway TEXT NOT NULL,
            connectionStatus TEXT,
            batteryLevel REAL
        )
    ''')

    # Tabla LocalSensor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LocalSensor (
            idSensor INTEGER PRIMARY KEY,
            idDevice INTEGER NOT NULL,
            frequency INTEGER,
            FOREIGN KEY (idDevice) REFERENCES LocalDevice(idLocalDevice)
        )
    ''')

    # Tabla LocalActuator
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LocalActuator (
            idActuator INTEGER PRIMARY KEY,
            idDevice INTEGER NOT NULL,
            status TEXT,
            FOREIGN KEY (idDevice) REFERENCES LocalDevice(idLocalDevice)
        )
    ''')

    # Tabla Measurement
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Measurement (
            idMeasurement INTEGER PRIMARY KEY,
            idSensor INTEGER NOT NULL,
            value REAL,
            timestamp TEXT,
            verification BOOLEAN DEFAULT 0,
            FOREIGN KEY (idSensor) REFERENCES LocalSensor(idSensor)
        )
    ''')

    # Tabla Actuation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Actuation (
            idActuation INTEGER PRIMARY KEY,
            idLocalActuator INTEGER NOT NULL,
            timestamp TEXT,
            value TEXT,
            actionDuration INTEGER,
            verification BOOLEAN DEFAULT 0,
            FOREIGN KEY (idLocalActuator) REFERENCES LocalActuator(idActuator)
        )
    ''')

    # Tabla LocalRuleEnergyConsumption (ya sin listas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LocalRuleEnergyConsumption (
            idLocalRuleEnergyConsumption INTEGER PRIMARY KEY,
            operatorRule TEXT,
            newFrequency REAL
        )
    ''')

    # Tabla LocalCondition con relación a una regla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LocalCondition (
            idCondition TEXT PRIMARY KEY,
            operatorCondition TEXT,
            expectedValue REAL,
            idRule INTEGER NOT NULL,
            FOREIGN KEY (idRule) REFERENCES LocalRuleEnergyConsumption(idLocalRuleEnergyConsumption)
        )
    ''')

    # Tabla intermedia DeviceRule
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeviceRule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idRule INTEGER NOT NULL,
            idDevice INTEGER NOT NULL,
            FOREIGN KEY (idRule) REFERENCES LocalRuleEnergyConsumption(idLocalRuleEnergyConsumption),
            FOREIGN KEY (idDevice) REFERENCES LocalDevice(idLocalDevice)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente.")

if __name__ == "__main__":
    crear_tablas()