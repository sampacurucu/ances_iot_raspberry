import threading
import time
import socket
from .sensor_config_listener import iniciar_escucha_sensor
from .rules_config_listener import iniciar_escucha_reglas
from .condition_config_listener import iniciar_escucha_condicion  # 👈 NUEVO IMPORT

# Variables de control de hilos
threads = {}
stop_flags = {}

# Verifica conexión a internet
def hay_conexion():
    try:
        socket.create_connection(("www.google.com", 80), timeout=10)
        return True
    except:
        return False

# Inicia hilos si no están corriendo
def iniciar_listeners():
    global threads, stop_flags

    if "sensor" not in threads or not threads["sensor"].is_alive():
        stop_flags["sensor"] = threading.Event()
        threads["sensor"] = threading.Thread(target=iniciar_escucha_sensor, args=(stop_flags["sensor"],))
        threads["sensor"].start()
    
    if "reglas" not in threads or not threads["reglas"].is_alive():
        stop_flags["reglas"] = threading.Event()
        threads["reglas"] = threading.Thread(target=iniciar_escucha_reglas, args=(stop_flags["reglas"],))
        threads["reglas"].start()
    
    if "condicion" not in threads or not threads["condicion"].is_alive():  # 👈 NUEVO BLOQUE
        stop_flags["condicion"] = threading.Event()
        threads["condicion"] = threading.Thread(target=iniciar_escucha_condicion, args=(stop_flags["condicion"],))
        threads["condicion"].start()

# Detiene hilos usando flags
def detener_listeners():
    for flag in stop_flags.values():
        flag.set()
    for t in threads.values():
        t.join()

# Bucle principal
def verificar_y_escuchar():
    conectados = False

    while True:
        if hay_conexion(): 
            if not conectados:
                print("Internet disponible. Iniciando listeners...")
                iniciar_listeners()
                conectados = True
        else:
            if conectados:
                print("Sin conexión. Deteniendo listeners...")
                detener_listeners()
                conectados = False
            time.sleep(60)

# Punto de entrada
if __name__ == "__main__":
    verificar_y_escuchar()