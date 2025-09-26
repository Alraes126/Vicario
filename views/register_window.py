import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.user_model import UserModel
from controllers.register_controller import RegisterController # Added import

class RegisterWindow:
    def __init__(self, root, db):
        # Inicializa la ventana de registro
        # Guarda la ventana principal (root) y la conexión a la base de datos (db)
        self.root = root
        self.db = db
        self.user_model = UserModel(db)
        self.controller = RegisterController(self, self.user_model) # Initialize Controller
        self.image_path = None # Added to store selected image path
        self.image_data = None # Added to store binary image data
        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de registro

        # Crea un marco (frame) principal para organizar los widgets
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configura el sistema de grillas (grid) para que se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Aquí se crea la etiqueta para el título de la ventana
        ttk.Label(frame, text="📝 Registro Nuevo Usuario", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        self.entries = {}
        fields = ["Nombre", "Email", "Contraseña", "Edad", "Celular", "Apodo"]

        # Crea las etiquetas y campos de entrada para el formulario de rejistro
        for i, field in enumerate(fields):
            # Crea la etiqueta para el campo actual (ej "Nombre:")
            ttk.Label(frame, text=f"{field}:").grid(row=i + 1, column=0, pady=5, padx=5, sticky="w")
            # Crea el campo de entrada para el dato actual
            entry = ttk.Entry(frame, width=30)
            if field == "Contraseña":
                # Oculta la contraseña mientras se escribe
                entry.config(show="*")
            entry.grid(row=i + 1, column=1, pady=5, padx=5)
            self.entries[field.lower()] = entry

        # --- Image Upload Widgets ---
        image_row = len(fields) + 1
        ttk.Label(frame, text="Imagen de Perfil:").grid(row=image_row, column=0, pady=5, padx=5, sticky="w")
        
        image_frame = ttk.Frame(frame)
        image_frame.grid(row=image_row, column=1, pady=5, padx=5, sticky="ew")
        
        self.image_label = ttk.Label(image_frame, text="Ninguna imagen seleccionada", anchor="w")
        self.image_label.pack(side="left", fill="x", expand=True)
        
        ttk.Button(image_frame, text="Seleccionar", command=self.select_image).pack(side="right")
        # --- End Image Upload Widgets ---

        # Aquí se crea el botón para registrar al nuevo usuario
        ttk.Button(frame, text="Registrar", command=self.register).grid(row=len(fields) + 2, column=0, columnspan=2, pady=20) # Adjusted row

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen de Perfil",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.* ")]
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.image_data = f.read() # Read binary data
                self.image_path = file_path # Keep path for display purposes
                self.image_label.config(text=file_path.split('/')[-1]) # Display only filename
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")
                self.image_data = None
                self.image_path = None
                self.image_label.config(text="Ninguna imagen seleccionada")
        else:
            self.image_data = None
            self.image_path = None
            self.image_label.config(text="Ninguna imagen seleccionada")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.image_data = None
        self.image_path = None
        self.image_label.config(text="Ninguna imagen seleccionada")

    def register(self):
        # Esta función se ejecuta al presionar el botón "Registrar"
        
        # Obtiene los datos de los campos de entrada
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        user_data = {
            'nombre': data['nombre'],
            'email': data['email'],
            'contraseña': data['contraseña'],
            'edad': data['edad'], # Pass as string, controller will convert
            'celular': data['celular'],
            'apodo': data['apodo'],
        }
        
        self.controller.register_user(user_data, self.image_data)