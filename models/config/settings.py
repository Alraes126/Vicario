import os # Importamos el módulo 'os' para interactuar con el sistema operativo,
          # especialmente para acceder a variables de entorno.
from dotenv import load_dotenv # Importamos 'load_dotenv' de la biblioteca 'python-dotenv'.
                               # Esta biblioteca nos permite cargar variables de entorno
                               # desde un archivo .env en nuestro proyecto.

load_dotenv() # Llamamos a esta función para cargar las variables de entorno
              # definidas en el archivo .env al entorno del sistema.

# --- Definición de la Clase Config ---
# Esta clase es un ejemplo del patrón de diseño "Singleton" o una clase de utilidad
# para centralizar la configuración de la aplicación.
# Contiene ajustes importantes, como los detalles de conexión a la base de datos.
class Config:
    # DB_CONFIG es un diccionario que almacena los parámetros de conexión a la base de datos.
    # Obtenemos estos valores de las variables de entorno para mantener la información sensible
    # (como contraseñas) fuera del código fuente y facilitar la configuración en diferentes entornos.
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),       # Dirección del servidor de la base de datos.
        'database': os.getenv('DB_NAME'),   # Nombre de la base de datos.
        'user': os.getenv('DB_USER'),       # Nombre de usuario para acceder a la base de datos.
        'password': os.getenv('DB_PASSWORD'), # Contraseña del usuario de la base de datos.
        'port': int(os.getenv('DB_PORT'))   # Puerto de conexión a la base de datos (convertido a entero).
    }
