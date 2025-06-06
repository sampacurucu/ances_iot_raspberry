import os
import sqlite3
import pika
import json
from data.models.LocalDevice import LocalDevice
from data.models.LocalSensor import LocalSensor
from data.models.EnergyRule import EnergyRule
from data.models.Condition import Condition

class DeviceController:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "AncesIoTLocalDatabase.db")
        self.url = "amqps://jzxjqutd:1kjOtKDpImcaUrPheRGx4ZEfROziWr6X@leopard.lmq.cloudamqp.com/jzxjqutd"

    # ────────────────────────────────────────────────
    # CONFIGURACIÓN DE SENSORES Y DISPOSITIVOS

    def existe_registro(self, cursor, tabla, campo, valor):
        cursor.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {campo} = ?", (valor,))
        return cursor.fetchone()[0] > 0

    def procesar_configuracion(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Procesar dispositivo
        device_data = data.get("device", {})
        device = LocalDevice(
            idLocalDevice=device_data.get("idLocalDevice"),
            idGateway=device_data.get("idGateway"),
            connectionStatus=device_data.get("connectionStatus"),
            batteryLevel=device_data.get("batteryLevel")
        )

        if self.existe_registro(cursor, "LocalDevice", "idLocalDevice", device.idLocalDevice):
            device.actualizar(cursor)
            print("Dispositivo actualizado:", device.__dict__)
        else:
            device.insertar(cursor)
            print("Dispositivo insertado:", device.__dict__)

        # Procesar sensor
        sensor_data = data.get("sensor", {})
        sensor = LocalSensor(
            idSensor=sensor_data.get("idSensor"),
            idDevice=sensor_data.get("idDevice"),
            frequency=sensor_data.get("frequency")
        )

        if self.existe_registro(cursor, "LocalSensor", "idSensor", sensor.idSensor):
            sensor.actualizar(cursor)
            print("Sensor actualizado:", sensor.__dict__)
        else:
            sensor.insertar(cursor)
            print("Sensor insertado:", sensor.__dict__)

        conn.commit()
        conn.close()

    # ────────────────────────────────────────────────
    # ENVÍO DE DATOS A LA COLA

    def conectar_db(self):
        return sqlite3.connect(self.db_path)

    def conectar_a_cola(self):
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        return channel, connection

    def enviar_mediciones(self):
        conn = self.conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Measurement WHERE verification = 0")
        mediciones = cursor.fetchall()

        if mediciones:
            channel, connection = self.conectar_a_cola()
            channel.queue_declare(queue='raspberry1/EnviarMediciones', durable=True)

            for medicion in mediciones:
                medicion_data = {
                    "idMeasurement": medicion[0],
                    "idSensor": medicion[1],
                    "value": medicion[2],
                    "timestamp": medicion[3],
                    "verification": medicion[4]
                }

                channel.basic_publish(
                    exchange='',
                    routing_key='raspberry1/EnviarMediciones',
                    body=json.dumps(medicion_data)
                )

                print(f"Medición enviada: {medicion_data}")

                cursor.execute("UPDATE Measurement SET verification = 1 WHERE idMeasurement = ?", (medicion[0],))
                conn.commit()

            connection.close()
        else:
            print("No hay nuevas mediciones para sincronizar.")

        conn.close()

    def enviar_actuaciones(self):
        conn = self.conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Actuation WHERE verification = 0")
        actuaciones = cursor.fetchall()

        if actuaciones:
            channel, connection = self.conectar_a_cola()
            channel.queue_declare(queue='actuaciones', durable=True)

            for actuacion in actuaciones:
                actuacion_data = {
                    "idActuation": actuacion[0],
                    "idLocalActuator": actuacion[1],
                    "timestamp": actuacion[2],
                    "value": actuacion[3],
                    "actionDuration": actuacion[4],
                    "verification": actuacion[5]
                }

                channel.basic_publish(
                    exchange='',
                    routing_key='actuaciones',
                    body=json.dumps(actuacion_data)
                )

                print(f"Actuación enviada: {actuacion_data}")

                cursor.execute("UPDATE Actuation SET verification = 1 WHERE idActuation = ?", (actuacion[0],))
                conn.commit()

            connection.close()
        else:
            print("No hay nuevas actuaciones para sincronizar.")

        conn.close()

    def enviar_datos_a_colas(self):
        self.enviar_mediciones()
        self.enviar_actuaciones()
        print("Sincronización completada.")
        
        
          # ────────────────────────────────────────────────
    # VALIDACION REGLAS
    def aplicar_reglas_energeticas(self):
        conn = self.conectar_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print("🔍 Buscando reglas energéticas en la base de datos...")
        cursor.execute("""
            SELECT * FROM LocalRuleEnergyConsumption
        """)
        reglas = cursor.fetchall()

        print(f"📋 Se encontraron {len(reglas)} regla(s) energética(s).")

        for regla in reglas:
            print("\n📌 Procesando regla:", regla)

            id_regla = regla['idLocalRuleEnergyConsumption']
            operador = regla['operatorRule']
            nueva_frecuencia = regla['newFrequency']  # Nueva frecuencia

            # Obtener los dispositivos afectados por esta regla
            cursor.execute("""
                SELECT dr.idDevice
                FROM DeviceRule dr
                WHERE dr.idRule = ?
            """, (id_regla,))
            dispositivos_afectados = cursor.fetchall()

            dispositivos_afectados = [d['idDevice'] for d in dispositivos_afectados]
            print(f"    Dispositivos afectados: {dispositivos_afectados}")

            # Obtener las condiciones asociadas a esta regla
            cursor.execute("""
                SELECT * FROM LocalCondition
                WHERE idRule = ?
            """, (id_regla,))
            condiciones = cursor.fetchall()

            # Evaluamos las condiciones para cada dispositivo afectado
            for id_device in dispositivos_afectados:
                print(f"  ⚙️ Verificando dispositivo ID: {id_device}")
                cursor.execute("""
                    SELECT d.idLocalDevice, d.batteryLevel, s.idSensor, s.frequency
                    FROM LocalDevice d
                    JOIN LocalSensor s ON d.idLocalDevice = s.idDevice
                    WHERE d.idLocalDevice = ?
                """, (id_device,))
                fila = cursor.fetchone()

                if fila:
                    idDispositivo = fila["idLocalDevice"]
                    batteryLevel = fila["batteryLevel"]
                    idSensor = fila["idSensor"]
                    frecuencia = fila["frequency"]

                    valores_dispositivo = {
                        "batteryLevel": batteryLevel
                    }

                    resultados = []

                    for condicion in condiciones:
                        operador_cond = condicion['operatorCondition']
                        valor_esperado = condicion['expectedValue']
                        campo = "batteryLevel"  # Actualmente solo soportamos batería, puedes agregar otros campos si es necesario

                        valor_actual = valores_dispositivo.get(campo)

                        if valor_actual is None:
                            print(f"    ⚠️ Campo '{campo}' no encontrado en el dispositivo.")
                            resultados.append(False)
                            continue

                        resultado = False
                        if operador_cond == '<':
                            resultado = valor_actual < valor_esperado
                        elif operador_cond == '>':
                            resultado = valor_actual > valor_esperado
                        elif operador_cond == '==':
                            resultado = valor_actual == valor_esperado
                        else:
                            print(f"    ⚠️ Operador no reconocido: {operador_cond}")
                            resultados.append(False)
                            continue

                        resultados.append(resultado)
                        print(f"    ✅ Evaluando condición: {campo} {operador_cond} {valor_esperado} -> {resultado}")

                    cumple_regla = all(resultados) if operador == 'AND' else any(resultados)
                    print(f"    🧠 Resultado global con operador {operador}: {cumple_regla}")

                    if cumple_regla:
                        if frecuencia != nueva_frecuencia:
                            cursor.execute("""
                                UPDATE LocalSensor SET frequency = ? WHERE idSensor = ?
                            """, (nueva_frecuencia, idSensor))
                            print(f"    ✅ Sensor {idSensor} actualizado a frecuencia {nueva_frecuencia}.")
                        else:
                            print(f"    🔁 Frecuencia ya está en {frecuencia}, no se actualiza.")
                    else:
                        print(f"    ❌ Regla no cumplida. Frecuencia no se actualiza, se mantiene en {frecuencia}.")
                else:
                    print(f"    ⚠️ No se encontró información para el dispositivo {id_device}.")

        conn.commit()
        conn.close()
        print("\n✅ Finalizó el procesamiento de reglas energéticas.")


    # ────────────────────────────────────────────────
# AGREGAR O MODIFICAR REGLA QUE LLEGA COLA
    def procesar_reglas(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Obtener la regla
        rule_data = data.get("rule", {})
        if not rule_data:
            print("❌ No se proporcionó información de la regla.")
            return

        # Crear objeto de la regla
        rule = EnergyRule(
            idLocalRuleEnergyConsumption=rule_data.get("idLocalRuleEnergyConsumption"),
            operatorRule=rule_data.get("operatorRule"),
            newFrequency=rule_data.get("newFrequency")
        )

        # Insertar o actualizar la regla
        if self.existe_registro(cursor, "LocalRuleEnergyConsumption", "idLocalRuleEnergyConsumption", rule.idLocalRuleEnergyConsumption):
            rule.actualizar(cursor)
            print("✅ Regla actualizada:", rule.__dict__)
        else:
            rule.insertar(cursor)
            print("✅ Regla insertada:", rule.__dict__)

        # Procesar los dispositivos asociados a la regla
        device_ids = rule_data.get("idDevice", [])
        if not isinstance(device_ids, list):
            print("⚠️ idDevice debe ser una lista. Valor recibido:", device_ids)
            device_ids = []

        # Eliminar las asociaciones que ya no estén en la lista
        cursor.execute("""
            DELETE FROM DeviceRule
            WHERE idRule = ? AND idDevice NOT IN (?)
        """, (rule.idLocalRuleEnergyConsumption, ','.join(map(str, device_ids))))
        print(f"✅ Asociaciones eliminadas para la regla {rule.idLocalRuleEnergyConsumption}, dispositivos no presentes: {device_ids}")

        # Insertar las nuevas asociaciones
        for device_id in device_ids:
            if self.existe_registro(cursor, "LocalDevice", "idLocalDevice", device_id):
                # Verifica si ya existe la asociación antes de insertarla
                cursor.execute("""
                    SELECT COUNT(*) FROM DeviceRule
                    WHERE idRule = ? AND idDevice = ?
                """, (rule.idLocalRuleEnergyConsumption, device_id))
                exists = cursor.fetchone()[0]

                if not exists:
                    cursor.execute(
                        '''
                        INSERT INTO DeviceRule (idRule, idDevice)
                        VALUES (?, ?)
                        ''',
                        (rule.idLocalRuleEnergyConsumption, device_id)
                    )
                    print(f"✅ Asociación insertada: regla {rule.idLocalRuleEnergyConsumption} ↔ dispositivo {device_id}")
                else:
                    print(f"⚠️ La asociación entre regla {rule.idLocalRuleEnergyConsumption} y dispositivo {device_id} ya existe.")
            else:
                print(f"⚠️ Dispositivo con ID {device_id} no existe en LocalDevice. Asociación ignorada.")

        conn.commit()
        conn.close()
        
        
        
        
    
    # ────────────────────────────────────────────────
# AGREGAR O MODIFICAR CONDICION QUE LLEGA COLA    
    def procesar_condiciones(self, condiciones_data):
        print("[INFO] Procesando condiciones recibidas...")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Si solo se envía una condición como diccionario simple
            if isinstance(condiciones_data, dict):
                condiciones_data = [condiciones_data]

            for condicion_json in condiciones_data:
                condicion = Condition(
                    idCondition=condicion_json["idCondition"],
                    operatorCondition=condicion_json["operatorCondition"],
                    expectedValue=condicion_json["expectedValue"],
                    idRule=condicion_json["idRule"]
                )

                # Intentar actualizar primero
                cursor.execute("SELECT COUNT(*) FROM LocalCondition WHERE idCondition = ?", (condicion.idCondition,))
                existe = cursor.fetchone()[0]

                if existe:
                    condicion.actualizar(cursor)
                    print(f"[INFO] Condición {condicion.idCondition} actualizada.")
                else:
                    condicion.insertar(cursor)
                    print(f"[INFO] Condición {condicion.idCondition} insertada.")

            conn.commit()
            print("[INFO] Todas las condiciones procesadas correctamente.")

        except Exception as e:
            print("[ERROR] Error al procesar condiciones:", e)

        finally:
            conn.close()
