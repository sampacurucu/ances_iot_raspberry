class DeviceRule:
    def __init__(self, id, idRule, idDevice):
        self.id = id
        self.idRule = idRule
        self.idDevice = idDevice

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO DeviceRule (id, idRule, idDevice)
            VALUES (?, ?, ?)
        """, (self.id, self.idRule, self.idDevice))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE DeviceRule
            SET idRule = ?, idDevice = ?
            WHERE id = ?
        """, (self.idRule, self.idDevice, self.id))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM DeviceRule WHERE id = ?
        """, (self.id,))