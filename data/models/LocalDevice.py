# models/local_device.py
class LocalDevice:
    def __init__(self, idLocalDevice, idGateway, connectionStatus, batteryLevel):
        self.idLocalDevice = idLocalDevice
        self.idGateway = idGateway
        self.connectionStatus = connectionStatus
        self.batteryLevel = batteryLevel

    def insertar(self, cursor):
        cursor.execute("""
            INSERT INTO LocalDevice (idLocalDevice, idGateway, connectionStatus, batteryLevel)
            VALUES (?, ?, ?, ?)
        """, (self.idLocalDevice, self.idGateway, self.connectionStatus, self.batteryLevel))

    def actualizar(self, cursor):
        cursor.execute("""
            UPDATE LocalDevice
            SET idGateway = ?, connectionStatus = ?, batteryLevel = ?
            WHERE idLocalDevice = ?
        """, (self.idGateway, self.connectionStatus, self.batteryLevel, self.idLocalDevice))

    def eliminar(self, cursor):
        cursor.execute("""
            DELETE FROM LocalDevice WHERE idLocalDevice = ?
        """, (self.idLocalDevice,))