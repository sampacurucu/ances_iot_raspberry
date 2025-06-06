# Logs/log_manager.py
import logging
import os
import sys

# Crear carpeta logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuración del logging
logging.basicConfig(
    filename='logs/sistema.log',  # Ruta donde se guardará el archivo de log
    level=logging.DEBUG,  # Nivel de logs que se registrarán
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Funciones para loguear mensajes
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)

def log_debug(message):
    logging.debug(message)

# Función que redirige los print a logs
class LogWriter:
    def write(self, message):
        logging.info(message.strip())

# Solo redirigir print si es necesario, no afecta a la ejecución normal
def redirect_print():
    sys.stdout = LogWriter()

# Desactivar redirección (si se desea)
def restore_print():
    sys.stdout = sys.__stdout__  # Restaurar el comportamiento por defecto de print