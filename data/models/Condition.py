import sqlite3
import json

class Condition:
    def __init__(self, idCondition, operatorCondition, expectedValue, idRule):
        self.idCondition = idCondition
        self.operatorCondition = operatorCondition
        self.expectedValue = expectedValue
        self.idRule = idRule

    def insertar(self, cursor):
        print("[DEBUG] Insertando Condición con:")
        print("  idCondition:", self.idCondition)
        print("  operatorCondition:", self.operatorCondition)
        print("  expectedValue:", self.expectedValue)
        print("  idRule:", self.idRule)

        cursor.execute("""
            INSERT INTO LocalCondition (idCondition, operatorCondition, expectedValue, idRule)
            VALUES (?, ?, ?, ?)
        """, (self.idCondition, self.operatorCondition, self.expectedValue, self.idRule))

    def actualizar(self, cursor):
        print("[DEBUG] Actualizando Condición con:")
        print("  idCondition:", self.idCondition)
        print("  operatorCondition:", self.operatorCondition)
        print("  expectedValue:", self.expectedValue)
        print("  idRule:", self.idRule)

        cursor.execute("""
            UPDATE LocalCondition
            SET operatorCondition = ?, expectedValue = ?, idRule = ?
            WHERE idCondition = ?
        """, (self.operatorCondition, self.expectedValue, self.idRule, self.idCondition))
