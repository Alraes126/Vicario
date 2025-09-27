import mysql.connector # Importamos la biblioteca para conectar Python con bases de datos MySQL.
from mysql.connector import Error # Importamos la clase Error para manejar excepciones específicas de MySQL.
from models.config.settings import Config # Importamos la configuración de la base de datos desde settings.py.


# --- Definición de la Clase DatabaseConnector ---
# Esta clase es responsable de gestionar la conexión con la base de datos MySQL
# y de ejecutar consultas. Es un ejemplo del patrón de diseño "Fachada" o "Singleton"
# para el acceso a la base de datos, centralizando la lógica de conexión.
class DatabaseConnector:
    # El constructor (__init__) se llama cuando creamos un objeto DatabaseConnector.
    def __init__(self):
        self.connection = None # Inicializamos la conexión como None (sin conexión activa).
        self.connect()         # Intentamos establecer la conexión inmediatamente.

    # Método para establecer la conexión con la base de datos.
    # Utiliza la configuración definida en 'settings.py'.
    def connect(self):
        try:
            # Hacemos una copia de la configuración de la base de datos para poder modificarla
            # (por ejemplo, añadir 'autocommit') sin afectar la configuración original.
            db_config = Config.DB_CONFIG.copy()
            # Con 'autocommit=True', cada comando que enviamos a la base de datos
            # se guarda (commit) automáticamente. Esto simplifica las transacciones.
            db_config['autocommit'] = True
            # Usamos 'mysql.connector.connect' para establecer la conexión,
            # pasando la configuración como argumentos clave-valor (**db_config).
            self.connection = mysql.connector.connect(**db_config)
            print("Conexión exitosa a la BD") # Mensaje de éxito en la consola.
        # Si ocurre algún error durante el intento de conexión, lo capturamos.
        except Error as e:
            print(f"Error de conexión: {e}") # Imprimimos el mensaje de error.

    # Método para ejecutar consultas de selección (SELECT) en la base de datos.
    # Devuelve los resultados de la consulta.
    def execute_query(self, query, params=None):
        try:
            # Creamos un 'cursor'. Un cursor es un objeto que nos permite ejecutar comandos SQL.
            # 'dictionary=True' hace que los resultados se devuelvan como diccionarios,
            # donde las claves son los nombres de las columnas.
            cursor = self.connection.cursor(dictionary=True)
            # Ejecutamos la consulta SQL. 'params or ()' maneja el caso donde no hay parámetros.
            cursor.execute(query, params or ())
            result = cursor.fetchall() # Obtenemos todos los resultados de la consulta.
            cursor.close()             # Cerramos el cursor para liberar recursos.
            return result              # Devolvemos los resultados.
        except Error as e: # Si ocurre un error durante la ejecución de la consulta, lo capturamos.
            print(f"Error en query: {e}") # Imprimimos el mensaje de error.
            return None                # Devolvemos None para indicar que hubo un fallo.

    # Método para ejecutar consultas de modificación (INSERT, UPDATE, DELETE) en la base de datos.
    # Devuelve True si la operación fue exitosa, False en caso contrario.
    def execute_update(self, query, params=None):
        try:
            # Creamos un cursor (sin 'dictionary=True' porque no esperamos resultados para estas operaciones).
            cursor = self.connection.cursor()
            cursor.execute(query, params or ()) # Ejecutamos la consulta.
            cursor.close()                     # Cerramos el cursor.
            return True                        # Indicamos éxito.
        except Error as e: # Si ocurre un error, lo capturamos.
            print(f"Error en update: {e}") # Imprimimos el mensaje de error.
            return False                       # Indicamos fallo.

    # Método para cerrar la conexión a la base de datos.
    # Es importante cerrar las conexiones cuando ya no se necesitan para liberar recursos.
    def disconnect(self):
        if self.connection: # Verificamos si la conexión está activa antes de intentar cerrarla.
            self.connection.close() # Cerramos la conexión.