import pika
import json
import os
import sys
import time
import traceback  # Para mostrar errores detallados

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
def procesar_condiciones(ch, method, properties, body):
    try:
        # Asegurarnos de que el cuerpo sea un diccionario JSON correctamente cargado
        data = json.loads(body)

        # Si el dato es un solo diccionario, convertirlo en una lista
        if isinstance(data, dict):
            data = [data]

        device_controller = DeviceController()
        device_controller.procesar_condiciones(data)
    except Exception as e:
        print("[Condición Listener] Error al procesar mensaje:")
        traceback.print_exc()

# Función que inicia la escucha, controlada por un stop_flag
def iniciar_escucha_condicion(stop_flag):
    try:
        channel, connection = conectar_a_cola()
        channel.queue_declare(queue='raspberry1/configuracion/condicion', durable=True)
        channel.basic_consume(queue='raspberry1/configuracion/condicion', on_message_callback=procesar_condiciones, auto_ack=True)

        print("[Condición Listener] Escuchando configuraciones de condiciones...")

        while not stop_flag.is_set():
            connection.process_data_events(time_limit=1)
            time.sleep(0.5)

        print("[Condición Listener] Detenido por pérdida de conexión.")
        channel.close()
        connection.close()

    except Exception as e:
        print("[Condición Listener] Error en listener:")
        traceback.print_exc()