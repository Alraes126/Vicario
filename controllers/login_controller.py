# controllers/login_controller.py
# Este archivo define el controlador para la funcionalidad de inicio de sesión.
# Un controlador gestiona la interacción del usuario con la vista de login
# y coordina con el modelo de usuario para autenticar credenciales.

# --- Importación de Bibliotecas ---
import re # Importamos el módulo 're' para trabajar con Expresiones Regulares (regex).
          # Las regex son útiles para validar formatos de texto, como direcciones de correo electrónico.
from tkinter import messagebox # Para mostrar mensajes emergentes (pop-ups) al usuario.

# --- Definición de la Clase LoginController ---
# Esta clase es un ejemplo del patrón de diseño MVC (Modelo-Vista-Controlador).
# Su responsabilidad es manejar la lógica de inicio de sesión.
class LoginController:
    # El constructor (__init__) inicializa el controlador con las dependencias necesarias.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, view, user_model):
        self.view = view             # La Vista asociada a este controlador (LoginWindow).
        self.user_model = user_model # El Modelo de Usuario para interactuar con los datos de usuario (autenticación).
        
        # Referencias a otros controladores. Se inicializan como None y se asignan más tarde.
        # Esto permite que, una vez que el usuario inicia sesión, este controlador pueda
        # notificar a otras partes de la aplicación sobre el usuario logueado.
        self.dashboard_controller = None
        self.slot_machine_controller = None
        self.bet_controller = None
        self.transaction_controller = None

    # Método principal para intentar iniciar sesión.
    # Recibe el email y la contraseña ingresados por el usuario.
    def login_user(self, email, password):
        # Primero, validamos que los campos de email y contraseña no estén vacíos.
        if not email or not password:
            messagebox.showerror("Error", "Email y contraseña son requeridos.")
            return False # Indicamos que el login falló.

        # --- Validación de Email con Expresión Regular ---
        # Definimos una expresión regular para verificar el formato del email.
        # Esto asegura que el email tenga una estructura válida (ej. usuario@dominio.com).
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email): # Usamos re.match para comparar el email con la regex.
            messagebox.showerror("Error", "El formato del email no es válido.")
            return False # Indicamos que el login falló.

        # Intentamos obtener el usuario de la base de datos usando el modelo.
        # El modelo se encarga de la lógica de acceso a datos.
        user = self.user_model.get_user_by_email_and_password(email, password)

        if user: # Si se encuentra un usuario con esas credenciales...
            messagebox.showinfo("Éxito", f"¡Bienvenido, {user['nombre']}!") # Mostramos un mensaje de bienvenida.
            
            # --- Propagación de Información del Usuario Logueado ---
            # Notificamos a todos los controladores relevantes sobre el usuario que acaba de iniciar sesión.
            # Esto es crucial para que otras partes de la aplicación puedan mostrar datos específicos del usuario.
            if self.dashboard_controller:
                self.dashboard_controller.set_current_user(user)
            if self.slot_machine_controller:
                self.slot_machine_controller.set_current_user(user)
            if self.bet_controller:
                self.bet_controller.set_current_user(user)
            if self.transaction_controller:
                self.transaction_controller.set_current_user(user)

            # Le decimos a la Vista de Login que el inicio de sesión fue exitoso.
            # La vista puede entonces, por ejemplo, cambiar a la pestaña del dashboard.
            self.view.on_login_success(user)
            return True # Indicamos que el login fue exitoso.
        else: # Si no se encuentra un usuario o las credenciales son incorrectas...
            messagebox.showerror("Error", "Email o contraseña incorrectos.")
            return False # Indicamos que el login falló.
