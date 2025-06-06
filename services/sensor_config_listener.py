import pika
import json
import os
import sys
import time

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
def procesar_configuracion(ch, method, properties, body):
    data = json.loads(body)
    device_controller = DeviceController()
    device_controller.procesar_configuracion(data)

# Nueva función que usa stop_flag
def iniciar_escucha_sensor(stop_flag):
    try:
        channel, connection = conectar_a_cola()
        channel.queue_declare(queue='raspberry1/configuracion/sensor', durable=True)
        channel.basic_consume(queue='raspberry1/configuracion/sensor', on_message_callback=procesar_configuracion, auto_ack=True)

        print("[Sensor Listener] Escuchando configuraciones...")

        # Bucle controlado por flag
        while not stop_flag.is_set():
            connection.process_data_events(time_limit=1)
            time.sleep(0.5)

        print("[Sensor Listener] Detenido por pérdida de conexión.")
        channel.close()
        connection.close()

    except Exception as e:
        print(f"[Sensor Listener] Error en listener: {e}")