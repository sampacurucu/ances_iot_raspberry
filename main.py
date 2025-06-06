# main.py
import threading
import time
from data.database import crear_tablas
from services.verificar_y_enviar import verificar_y_enviar
from services.verificar_y_escuchar import verificar_y_escuchar  # Importa la función
from data.limpieza_mediciones_actuaciones import eliminar_mediciones_antiguas, eliminar_actuaciones_antiguas
from core.device_controller import DeviceController  # Asegúrate de importar
#from logs.log_manager import log_info, log_error, log_warning, log_debug


# Función principal que se ejecuta al inicio
def main():
    # Llamar a la función para crear las tablas
    #crear_tablas()
    
    # Iniciar los hilos
    iniciar_verificacion()
    #iniciar_verificacion_y_escucha()  # Inicia la verificación y escucha
    #iniciar_limpieza_periodica()
    #iniciar_reglas_energeticas()
    # Mantener el proceso principal en ejecución
    while True:
        #print("Main ejecutándose, todo está bien.")
        time.sleep(10)  # Esta parte puede hacer otras tareas o simplemente mantener vivo el programa


# Función para iniciar el hilo de verificación y envío
def iniciar_verificacion():
    t = threading.Thread(target=verificar_y_enviar)
    t.daemon = True  # Asegura que el hilo se termine cuando el programa principal termine
    t.start()


# Función para iniciar el hilo de verificación y escucha
def iniciar_verificacion_y_escucha():
    t = threading.Thread(target=verificar_y_escuchar)
    t.daemon = True  # Asegura que el hilo se termine cuando el programa principal termine
    t.start()


# Función para iniciar el hilo de limpieza periódica (una vez al día)
def iniciar_limpieza_periodica():
    def limpieza_periodica():
        while True:
            eliminar_mediciones_antiguas()
            eliminar_actuaciones_antiguas()
            time.sleep(86400)  # Esperar 1 día (en segundos)

    t = threading.Thread(target=limpieza_periodica)
    t.daemon = True
    t.start()


def iniciar_reglas_energeticas():
    def ejecutar_reglas():
        controller = DeviceController()
        while True:
            print("Ejecutando evaluación de reglas energéticas...")
            controller.aplicar_reglas_energeticas()
            time.sleep(3600)  # Esperar 1 hora

    t = threading.Thread(target=ejecutar_reglas)
    t.daemon = True
    t.start()
    
# Punto de entrada principal
if __name__ == "__main__":
    main()