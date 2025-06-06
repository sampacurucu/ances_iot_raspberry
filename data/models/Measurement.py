# models/measurement.py
class Measurement:
    def __init__(self, idMeasurement, idSensor, value, timestamp, verification):
        self.idMeasurement = idMeasurement
        self.idSensor = idSensor
        self.value = value
        self.timestamp = timestamp
        self.verification = verification

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO Measurement (idMeasurement, idSensor, value, timestamp, verification)
            VALUES (?, ?, ?, ?, ?)
        """, (self.idMeasurement, self.idSensor, self.value, self.timestamp, self.verification))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE Measurement
            SET idSensor = ?, value = ?, timestamp = ?, verification = ?
            WHERE idMeasurement = ?
        """, (self.idSensor, self.value, self.timestamp, self.verification, self.idMeasurement))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM Measurement WHERE idMeasurement = ?
        """, (self.idMeasurement,))
