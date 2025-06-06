import pika
import json
import os
import sys
import time
import traceback  # <-- Importante para mostrar errores completos

# Agregar la carpeta AncesIoT al path de búsqueda de módulos
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core.device_controller import DeviceController  # Importamos el controlador

# Conectar a RabbitMQ
def conectar_a_cola():
    url = "amqps://jzxjqutd:1kjOtKDpImcaUrPheRGx4ZEfROziWr6X@leopard.lmq.cloudamqp.com/jzxjqutd"
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return channel, connection

# Procesar mensaje recibido
def procesar_reglas(ch, method, properties, body):
    try:
        data = json.loads(body)
        device_controller = DeviceController()
        device_controller.procesar_reglas(data)
    except Exception as e:
        print("[Reglas Listener] Error al procesar mensaje:")
        traceback.print_exc()  # Muestra traza completa del error

# Nueva función que usa stop_flag
def iniciar_escucha_reglas(stop_flag):
    try:
        channel, connection = conectar_a_cola()
        channel.queue_declare(queue='raspberry1/configuracion/regla', durable=True)
        channel.basic_consume(queue='raspberry1/configuracion/regla', on_message_callback=procesar_reglas, auto_ack=True)

        print("[Reglas Listener] Escuchando configuraciones de reglas...")

        # Bucle controlado por flag
        while not stop_flag.is_set():
            connection.process_data_events(time_limit=1)
            time.sleep(0.5)

        print("[Reglas Listener] Detenido por pérdida de conexión.")
        channel.close()
        connection.close()

    except Exception as e:
        print("[Reglas Listener] Error en listener:")
        traceback.print_exc()  # Muestra traza completa del error