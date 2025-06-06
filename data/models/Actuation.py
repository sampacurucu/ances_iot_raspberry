# models/actuation.py
class Actuation:
    def __init__(self, idActuation, idLocalActuator, timestamp, value, actionDuration, verification):
        self.idActuation = idActuation
        self.idLocalActuator = idLocalActuator
        self.timestamp = timestamp
        self.value = value
        self.actionDuration = actionDuration
        self.verification = verification

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO Actuation (idActuation, idLocalActuator, timestamp, value, actionDuration, verification)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.idActuation, self.idLocalActuator, self.timestamp, self.value, self.actionDuration, self.verification))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE Actuation
            SET idLocalActuator = ?, timestamp = ?, value = ?, actionDuration = ?, verification = ?
            WHERE idActuation = ?
        """, (self.idLocalActuator, self.timestamp, self.value, self.actionDuration, self.verification, self.idActuation))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM Actuation WHERE idActuation = ?
        """, (self.idActuation,))
