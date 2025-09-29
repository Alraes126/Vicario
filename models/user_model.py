from models.Database.database_manager import DatabaseConnector # Importamos el conector de la base de datos.
from PIL import Image # Importamos la clase Image de la biblioteca Pillow (PIL) para manipular imágenes.
import io # Importamos el módulo 'io' para trabajar con datos binarios de la imagen en memoria.

# --- Definición de la Clase UserModel ---
# Esta clase es el Modelo para la gestión de datos de usuarios.
# Un modelo es responsable de interactuar con la base de datos para
# almacenar, recuperar y manipular la información de los usuarios, incluyendo su perfil.
class UserModel:
    # El constructor (__init__) inicializa el modelo con un conector a la base de datos.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, db_connector):
        self.db = db_connector # Almacena la instancia del conector de la base de datos.

    # Método para crear un nuevo usuario en la base de datos.
    # Recibe los datos del usuario y, opcionalmente, los datos binarios de una imagen de perfil.
    def create_user(self, user_data, image_data=None):
        processed_image_data = None # Variable para guardar la imagen procesada (más pequeña).
        if image_data: # Si se proporcionaron datos de imagen...
            try:
                # 1. Abrir la imagen desde los datos binarios que vienen de la interfaz.
                # 'io.BytesIO' permite a Pillow leer los bytes como si fuera un archivo.
                img = Image.open(io.BytesIO(image_data))
                
                # 2. Definir un tamaño máximo para la imagen de perfil (ej. 200x200 píxeles).
                max_size = (200, 200)

                # 3. Redimensionar la imagen manteniendo su proporción original.
                # 'img.thumbnail' ajusta la imagen para que quepa en 'max_size'.
                # 'Image.Resampling.LANCZOS' es un filtro de alta calidad para el redimensionamiento.
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Convertir a modo RGB si la imagen está en RGBA (con canal alfa),
                # ya que JPEG no soporta canales alfa.
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # 4. Convertir la imagen redimensionada de nuevo a datos binarios.
                # La guardamos en formato JPEG para una buena compresión.
                byte_arr = io.BytesIO()
                img.save(byte_arr, format='JPEG')
                processed_image_data = byte_arr.getvalue() # Obtenemos los bytes finales de la imagen.
            except Exception as e:
                # Si hay un error al procesar la imagen (ej. no es un formato válido),
                # imprimimos el error y no guardamos la imagen.
                print(f"Error al procesar la imagen: {e}")
                processed_image_data = None
        
        # Asignamos los datos de la imagen (procesados o None) a la información del usuario.
        user_data['ruta_imagen'] = processed_image_data
        # DEBUG: Imprimimos la longitud de los datos de la imagen procesada para depuración.
        print(f"DEBUG: UserModel - processed_image_data length: {len(processed_image_data) if processed_image_data else 'None'}")

        # --- Preparar la Consulta SQL para Insertar el Nuevo Usuario ---
        # Extraemos los datos del diccionario user_data.
        nombre = user_data.get('nombre')
        email = user_data.get('email')
        contraseña = user_data.get('contraseña')
        edad = user_data.get('edad')
        celular = user_data.get('celular')
        apodo = user_data.get('apodo')
        ruta_imagen = user_data.get('ruta_imagen') # Esto serán los datos binarios o None.

        query = """
        INSERT INTO usuarios (nombre, tipo_usuario, saldo, correo, celular, edad, apodo, fecha_registro, estado, contraseña, ruta_imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, DEFAULT, %s, %s, %s)
        """
        # Definimos valores por defecto para un nuevo usuario.
        tipo_usuario = 'usuario'
        saldo = 0.00
        estado = 'activo'

        # Creamos una tupla con los parámetros para la consulta SQL.
        params = (
            nombre, tipo_usuario, saldo, email, celular, edad, apodo, estado, contraseña, ruta_imagen
        )

        # Ejecutamos la consulta de inserción en la base de datos.
        # El método 'execute_update' del conector de la base de datos maneja la ejecución.
        success = self.db.execute_update(query, params)
        return success # Devolvemos True si la inserción fue exitosa, False en caso contrario.

    # Método para obtener un usuario por su email y contraseña (para el login).
    def get_user_by_email_and_password(self, email, password):
        query = "SELECT idcedula, nombre, tipo_usuario, saldo, correo, celular, edad, apodo, fecha_registro, estado, ruta_imagen FROM usuarios WHERE correo = %s AND contraseña = %s"
        result = self.db.execute_query(query, (email, password)) # Ejecutamos la consulta.
        return result[0] if result else None # Devuelve el primer usuario encontrado o None.
