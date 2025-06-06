# models/local_actuator.py
class LocalActuator:
    def __init__(self, idLocalActuator, idLocalDevice, name, type):
        self.idLocalActuator = idLocalActuator
        self.idLocalDevice = idLocalDevice
        self.name = name
        self.type = type

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO LocalActuator (idLocalActuator, idLocalDevice, name, type)
            VALUES (?, ?, ?, ?)
        """, (self.idLocalActuator, self.idLocalDevice, self.name, self.type))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE LocalActuator
            SET idLocalDevice = ?, name = ?, type = ?
            WHERE idLocalActuator = ?
        """, (self.idLocalDevice, self.name, self.type, self.idLocalActuator))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM LocalActuator WHERE idLocalActuator = ?
        """, (self.idLocalActuator,))