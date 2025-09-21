import mysql.connector
from mysql.connector import Error


class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Cambiar por tus credenciales
                password='',
                database='casino_vicarios',
                autocommit=True
            )
            print("Conexión exitosa a la BD")
        except Error as e:
            print(f"Error de conexión: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error en query: {e}")
            return None

    def execute_update(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            cursor.close()
            return True
        except Error as e:
            print(f"Error en update: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()