import sqlite3

class EnergyRule:
    def __init__(self, idLocalRuleEnergyConsumption, operatorRule, newFrequency):
        self.idLocalRuleEnergyConsumption = idLocalRuleEnergyConsumption
        self.operatorRule = operatorRule
        self.newFrequency = newFrequency

    @staticmethod
    def from_row(row):
        return EnergyRule(
            idLocalRuleEnergyConsumption=row[0],
            operatorRule=row[1],
            newFrequency=row[2]
        )

    @staticmethod
    def obtener_todas(cursor):
        cursor.execute("SELECT * FROM LocalRuleEnergyConsumption")
        rows = cursor.fetchall()
        return [EnergyRule.from_row(row) for row in rows]

    def insertar(self, cursor):
        print("[DEBUG] Insertando EnergyRule con:")
        print("  idLocalRuleEnergyConsumption:", self.idLocalRuleEnergyConsumption)
        print("  operatorRule:", self.operatorRule)
        print("  newFrequency:", self.newFrequency)

        self._validar_y_convertir()

        try:
            cursor.execute("""
                INSERT INTO LocalRuleEnergyConsumption (
                    idLocalRuleEnergyConsumption,
                    operatorRule,
                    newFrequency
                ) VALUES (?, ?, ?)
            """, (
                self.idLocalRuleEnergyConsumption,
                self.operatorRule,
                self.newFrequency
            ))
            print("Regla insertada correctamente")
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al insertar la regla: {e}")
        except Exception as e:
            print(f"Error al insertar la regla: {e}")

    def actualizar(self, cursor):
        print("[DEBUG] Actualizando EnergyRule con:")
        print("  idLocalRuleEnergyConsumption:", self.idLocalRuleEnergyConsumption)
        print("  operatorRule:", self.operatorRule)
        print("  newFrequency:", self.newFrequency)

        self._validar_y_convertir()

        try:
            cursor.execute("""
                UPDATE LocalRuleEnergyConsumption
                SET operatorRule = ?, newFrequency = ?
                WHERE idLocalRuleEnergyConsumption = ?
            """, (
                self.operatorRule,
                self.newFrequency,
                self.idLocalRuleEnergyConsumption
            ))
            print("Regla actualizada correctamente")
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al actualizar la regla: {e}")
        except Exception as e:
            print(f"Error al actualizar la regla: {e}")

    def _validar_y_convertir(self):
        if not isinstance(self.newFrequency, int):
            try:
                self.newFrequency = int(self.newFrequency)
            except Exception as e:
                raise ValueError(f"[ERROR] 'newFrequency' no es convertible a entero: {self.newFrequency}") from e