import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """
    Clase de configuración para centralizar los parámetros de la aplicación.
    Lee las credenciales de la base de datos desde variables de entorno
    para mayor seguridad y flexibilidad.
    """
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'casino_vicario')
    }