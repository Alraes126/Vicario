import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk, messagebox # Importamos ttk para widgets con estilos modernos y messagebox para mensajes emergentes.

# Importamos los Modelos y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from controllers.login_controller import LoginController

# --- Definición de la Clase LoginWindow ---
# Esta clase representa la Vista (GUI) para la pantalla de inicio de sesión.
# Es responsable de cómo se ve el formulario de login y cómo el usuario interactúa con él.
class LoginWindow:
    # El constructor (__init__) inicializa la ventana de login.
    # Recibe la ventana raíz, el conector de la base de datos y el widget de pestañas.
    def __init__(self, root, db, notebook):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        self.notebook = notebook     # El widget de pestañas (ttk.Notebook) para cambiar entre vistas.
        
        # Inicializamos el Modelo de Usuario.
        self.user_model = UserModel(db)
        # Creamos una instancia del Controlador de Login, pasándole esta vista y el modelo.
        # Esto establece la conexión entre la Vista y su Controlador.
        self.controller = LoginController(self, self.user_model)
        
        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.

    # Método para crear y organizar todos los widgets (campos de entrada, botones) de la ventana.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal para organizar los elementos.
        frame.grid(row=0, column=0, sticky="nsew") # Usamos grid para posicionar el marco.

        # Configuramos el sistema de grillas para que el marco se expanda correctamente.
        self.root.grid_row_configure(0, weight=1)
        self.root.grid_column_configure(0, weight=1)

        # Etiqueta de título para la ventana de login.
        ttk.Label(frame, text="🎰 CASINO VICARIO", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Etiqueta y campo de entrada para el email.
        ttk.Label(frame, text="Email:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.email = ttk.Entry(frame, width=30)
        self.email.grid(row=1, column=1, pady=5, padx=5)

        # Etiqueta y campo de entrada para la contraseña.
        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.password = ttk.Entry(frame, width=30, show="*") # 'show="*"' oculta los caracteres de la contraseña.
        self.password.grid(row=2, column=1, pady=5, padx=5)

        # Botón para iniciar sesión. Al hacer clic, llama al método 'login'.
        ttk.Button(frame, text="Ingresar", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botón para cambiar a la ventana de registro. Al hacer clic, llama al método 'open_register'.
        ttk.Button(frame, text="Registrar", command=self.open_register).grid(row=4, column=0, columnspan=2, pady=5)

    # Método que se ejecuta cuando el usuario hace clic en el botón "Ingresar".
    def login(self):
        email = self.email.get()     # Obtenemos el email del campo de entrada.
        password = self.password.get() # Obtenemos la contraseña del campo de entrada.
        # Le pedimos al controlador que intente iniciar sesión con estas credenciales.
        self.controller.login_user(email, password)

    # Método que se llama desde el controlador cuando el inicio de sesión es exitoso.
    def on_login_success(self, user):
        messagebox.showinfo("Login", f"¡Bienvenido, {user['nombre']}!") # Mostramos un mensaje de bienvenida.
        self.email.delete(0, tk.END)     # Limpiamos el campo de email.
        self.password.delete(0, tk.END) # Limpiamos el campo de contraseña.
        self.notebook.select(2)         # Cambiamos a la pestaña del Dashboard (asumiendo que es la tercera pestaña, índice 2).
        
        # Si el controlador tiene una referencia al controlador del dashboard,
        # le pasamos los datos del usuario para que el dashboard se actualice.
        if hasattr(self.controller, 'dashboard_controller') and self.controller.dashboard_controller:
            self.controller.dashboard_controller.set_current_user(user)

    # Método que se ejecuta cuando el usuario hace clic en el botón "Registrar".
    def open_register(self):
        # Cambiamos a la pestaña de Registro (asumiendo que es la segunda pestaña, índice 1).
        self.notebook.select(1)