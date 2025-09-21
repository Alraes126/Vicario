import os
from dotenv import load_dotenv

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'casino_vicarios'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', 3306))
    }