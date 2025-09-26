import tkinter as tk
from tkinter import ttk, messagebox
from models.user_model import UserModel # Added import
from controllers.login_controller import LoginController # Added import

class LoginWindow:
    def __init__(self, root, db, notebook):
        # Inicializa la ventana de login
        # Guarda la ventana principal (root) la conexión a la base de datos (db)
        # y el widget de pestañas (notebook)
        self.root = root
        self.db = db
        self.notebook = notebook
        self.user_model = UserModel(db) # Initialize UserModel
        self.controller = LoginController(self, self.user_model) # Initialize Controller
        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de login

        # Crea un marco (frame) principal para organizar los widgets
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configura el sistema de grillas (grid) para que se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Aquí se crea la etiqueta para el título de la ventana
        ttk.Label(frame, text="🎰 CASINO VICARIO", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Aquí se crea la etiqueta para el campo de email
        ttk.Label(frame, text="Email:").grid(row=1, column=0, pady=5, padx=5, sticky="w")

        # Aquí se crea el campo de entrada para el email
        self.email = ttk.Entry(frame, width=30)
        self.email.grid(row=1, column=1, pady=5, padx=5)

        # Aquí se crea la etiqueta para el campo de contraseña
        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        
        # Aquí se crea el campo de entrada para la contraseña
        self.password = ttk.Entry(frame, width=30, show="*")
        self.password.grid(row=2, column=1, pady=5, padx=5)

        # Aquí se crea el botón para iniciar sesión
        ttk.Button(frame, text="Ingresar", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Aquí se crea el botón para abrir la ventana de rejistro
        ttk.Button(frame, text="Registrar", command=self.open_register).grid(row=4, column=0, columnspan=2, pady=5)

    def login(self):
        email = self.email.get()
        password = self.password.get()
        self.controller.login_user(email, password)

    def on_login_success(self, user): # Corrected syntax
        messagebox.showinfo("Login", f"¡Bienvenido, {user['nombre']}!")
        self.email.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.notebook.select(2) # Select Dashboard tab
        
        # Pass user data to the dashboard controller
        if hasattr(self.controller, 'dashboard_controller') and self.controller.dashboard_controller:
            self.controller.dashboard_controller.set_current_user(user)

    def open_register(self):
        # Esta función sirve para cambiar a la pestaña de registro
        self.notebook.select(1) # Asume que la de Registro es la segunda pestaña (índice 1)
