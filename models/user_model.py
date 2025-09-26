from models.Database.database_manager import DatabaseConnector
from PIL import Image # Necesario para manipular imágenes (redimensionar, comprimir)
import io # Necesario para trabajar con datos binarios de la imagen en memoria

class UserModel:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_user(self, user_data, image_data=None):
        # Variable para guardar la imagen procesada (más pequeña)
        processed_image_data = None
        if image_data:
            try:
                # 1. Abrir la imagen desde los datos binarios que vienen de la interfaz
                # io.BytesIO permite a Pillow leer los bytes como si fuera un archivo
                img = Image.open(io.BytesIO(image_data))
                
                # 2. Definir un tamaño máximo para la imagen de perfil
                max_size = (200, 200) # Por ejemplo, 200x200 píxeles

                # 3. Redimensionar la imagen manteniendo su proporción original
                # img.thumbnail ajusta la imagen para que quepa en max_size
                img.thumbnail(max_size, Image.Resampling.LANCZOS) # LANCZOS es un filtro de alta calidad

                # 4. Convertir la imagen redimensionada de nuevo a datos binarios
                # La guardamos en formato JPEG para una buena compresión
                byte_arr = io.BytesIO()
                img.save(byte_arr, format='JPEG')
                processed_image_data = byte_arr.getvalue() # Obtenemos los bytes finales
            except Exception as e:
                # Si hay un error al procesar la imagen (ej. no es un formato válido)
                print(f"Error al procesar la imagen: {e}")
                processed_image_data = None # No guardamos imagen si hay error
        
        # Asignamos los datos de la imagen (procesados o None) a la información del usuario
        user_data['ruta_imagen'] = processed_image_data

        # Preparar la consulta SQL para insertar el nuevo usuario
        nombre = user_data.get('nombre')
        email = user_data.get('email')
        contraseña = user_data.get('contraseña')
        edad = user_data.get('edad')
        celular = user_data.get('celular')
        apodo = user_data.get('apodo')
        ruta_imagen = user_data.get('ruta_imagen') # Esto serán los datos binarios o None

        query = """
        INSERT INTO usuarios (nombre, tipo_usuario, saldo, correo, celular, edad, apodo, fecha_registro, estado, contraseña, ruta_imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, DEFAULT, %s, %s, %s)
        """
        # Valores por defecto para un nuevo usuario
        tipo_usuario = 'usuario'
        saldo = 0.00
        estado = 'activo'

        params = (
            nombre, tipo_usuario, saldo, email, celular, edad, apodo, estado, contraseña, ruta_imagen
        )

        # Ejecutar la consulta en la base de datos
        success = self.db.execute_update(query, params)
        return success

    def get_user_by_email_and_password(self, email, password):
        query = "SELECT idcedula, nombre, tipo_usuario, saldo, correo, celular, edad, apodo, fecha_registro, estado, ruta_imagen FROM usuarios WHERE correo = %s AND contraseña = %s"
        result = self.db.execute_query(query, (email, password))
        return result[0] if result else None

    def get_user_by_id(self, user_id):
        query = "SELECT idcedula, nombre, tipo_usuario, saldo, correo, celular, edad, apodo, fecha_registro, estado, ruta_imagen FROM usuarios WHERE idcedula = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result else None

    def update_user_balance(self, user_id, new_balance):
        query = "UPDATE usuarios SET saldo = %s WHERE idcedula = %s"
        return self.db.execute_update(query, (new_balance, user_id))

