import mysql.connector
from mysql.connector import Error
from models.config.settings import Config


# Gestiona la conexión con la base de datos y la ejecución de consultas.
class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.connect()

    # Establece la conexión con la base de datos usando la configuración de settings.py.
    def connect(self):
        try:
            # Hacemos una copia de la configuración para poder modificarla sin afectar la original.
            db_config = Config.DB_CONFIG.copy()
            # Con autocommit=True, cada orden que le damos a la BD se guarda al instante.
            db_config['autocommit'] = True
            # Usamos la configuración para decirle a mysql.connector a dónde y cómo conectarse.
            self.connection = mysql.connector.connect(**db_config)
            print("Conexión exitosa a la BD")
        # Si algo sale mal durante la conexión, este bloque se activa y muestra el error.
        except Error as e:
            print(f"Error de conexión: {e}")

    # Ejecuta una consulta de selección (SELECT) y devuelve los resultados.
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

    # Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE).
    def execute_update(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            cursor.close()
            return True
        except Error as e:
            print(f"Error en update: {e}")
            return False

    # Cierra la conexión a la base de datos.
    def disconnect(self):
        if self.connection:
            self.connection.close()
