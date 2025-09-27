# controllers/register_controller.py
# Este archivo define el controlador para la funcionalidad de registro de nuevos usuarios.
# Un controlador gestiona la interacción del usuario con la vista de registro
# y coordina con el modelo de usuario para crear nuevas cuentas.

# --- Importación de Bibliotecas ---
import re # Importamos el módulo 're' para trabajar con Expresiones Regulares (regex).
          # Las regex son útiles para validar formatos de texto, como direcciones de correo electrónico y nombres.
from tkinter import messagebox # Para mostrar mensajes emergentes (pop-ups) al usuario.
from datetime import datetime  # Importamos 'datetime' para trabajar con fechas y calcular la edad.

# --- Definición de la Clase RegisterController ---
# Esta clase es un ejemplo del patrón de diseño MVC (Modelo-Vista-Controlador).
# Su responsabilidad es manejar la lógica de registro de usuarios.
class RegisterController:
    # El constructor (__init__) inicializa el controlador con las dependencias necesarias.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, view, user_model):
        self.view = view             # La Vista asociada a este controlador (RegisterWindow).
        self.user_model = user_model # El Modelo de Usuario para interactuar con los datos de usuario (creación).

    # Método principal para intentar registrar un nuevo usuario.
    # Recibe los datos del formulario de registro y los datos binarios de la imagen de perfil.
    def register_user(self, user_data, image_data):
        # --- Validación de Campos ---
        # 1. Validamos que todos los campos requeridos no estén vacíos.
        if not all(user_data.values()):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False # Indicamos que el registro falló.

        # 2. Validación de email con expresión regular.
        # Aseguramos que el email tenga un formato válido.
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, user_data['email']):
            messagebox.showerror("Error", "El formato del email no es válido.")
            return False

        # 3. Validación de longitud y caracteres para nombre y apodo.
        # Aseguramos que estos campos cumplan con ciertos criterios de longitud y contenido.
        for field in ['nombre', 'apodo']:
            if len(user_data[field]) < 2 or len(user_data[field]) > 50:
                messagebox.showerror("Error", f"El {field} debe tener entre 2 y 50 caracteres.")
                return False
            # Permitimos letras, números, espacios y guiones bajos.
            if not re.match(r'^[a-zA-Z0-9_ ]*$', user_data[field]):
                messagebox.showerror("Error", f"El {field} solo puede contener letras, números, espacios y guiones bajos.")
                return False

        # 4. Validación de longitud para la contraseña.
        # Aseguramos que la contraseña tenga una longitud mínima para mayor seguridad.
        if len(user_data['contraseña']) < 8:
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
            return False

        # 5. Validación de celular (solo números).
        # Aseguramos que el número de celular contenga solo dígitos.
        if not user_data['celular'].isdigit():
            messagebox.showerror("Error", "El celular solo debe contener números.")
            return False
        
        # 6. Validación de edad basada en la fecha de nacimiento.
        # Calculamos la edad a partir de la fecha de nacimiento proporcionada.
        try:
            # Convertimos la cadena de fecha a un objeto datetime.
            birth_date = datetime.strptime(user_data['edad'], '%Y-%m-%d')
            today = datetime.today() # Obtenemos la fecha actual.
            # Calculamos la edad.
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18: # Verificamos que el usuario sea mayor de 18 años.
                messagebox.showerror("Error", "Debes ser mayor de 18 años para registrarte.")
                return False
            user_data['edad'] = age # Actualizamos la edad en los datos del usuario.
        except ValueError: # Capturamos errores si el formato de fecha es incorrecto.
            messagebox.showerror("Error", "Formato de fecha de nacimiento inválido.")
            return False

        # --- Creación del Usuario en el Modelo ---
        # Si todas las validaciones pasan, llamamos al modelo para crear el usuario en la base de datos.
        # El modelo encapsula la lógica de persistencia de datos.
        success = self.user_model.create_user(user_data, image_data)

        if success: # Si el modelo reporta que el usuario fue creado exitosamente...
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente!")
            self.view.clear_form() # Le decimos a la Vista que limpie el formulario.
            return True # Indicamos que el registro fue exitoso.
        else: # Si el modelo reporta un fallo (ej. email o cédula ya existen)...
            messagebox.showerror("Error", "No se pudo registrar el usuario. El email o la cédula ya podrían existir.")
            return False # Indicamos que el registro falló.
