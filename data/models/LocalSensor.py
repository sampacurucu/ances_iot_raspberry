class LocalSensor:
    def __init__(self, idSensor, idDevice, frequency):
        self.idSensor = idSensor
        self.idDevice = idDevice
        self.frequency = frequency

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO LocalSensor (idSensor, idDevice, frequency)
            VALUES (?, ?, ?)
        """, (self.idSensor, self.idDevice, self.frequency))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE LocalSensor
            SET idDevice = ?, frequency = ?
            WHERE idSensor = ?
        """, (self.idDevice, self.frequency, self.idSensor))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM LocalSensor WHERE idSensor = ?
        """, (self.idSensor,))