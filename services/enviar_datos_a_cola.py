import os
import sys

# Asegurar acceso al core
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core.device_controller import DeviceController

if __name__ == "__main__":
    controller = DeviceController()
    controller.enviar_datos_a_colas()