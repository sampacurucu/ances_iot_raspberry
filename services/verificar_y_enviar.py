import socket
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.device_controller import DeviceController  # ← Cambiar la importación

# Función para verificar la conexión a internet
def verificar_conexion():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False

# Función principal
def verificar_y_enviar():
    controller = DeviceController()  # ← Crear una instancia del controlador

    while True:
        if verificar_conexion():
            print("Conexión a Internet detectada. Enviando datos a la cola...")
            controller.enviar_datos_a_colas()  # ← Llamar método del controlador
            #time.sleep(600)
            time.sleep(20)
        else:
            print("Sin conexión a Internet... reintento en 1 hora.")
           # time.sleep(3600)
            time.sleep(10)

# Punto de entrada
if __name__ == "__main__":
    verificar_y_enviar()