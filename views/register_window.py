
import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk, messagebox, filedialog # Importamos ttk para widgets con estilos modernos, messagebox para mensajes emergentes, y filedialog para abrir diálogos de selección de archivo.
from tkcalendar import DateEntry # Importamos DateEntry de tkcalendar para un selector de fechas amigable.

# Importamos el Modelo y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from controllers.register_controller import RegisterController

# --- Definición de la Clase RegisterWindow ---
# Esta clase representa la Vista (GUI) para la pantalla de registro de usuarios.
# Es responsable de cómo se ve el formulario de registro y cómo el usuario interactúa con él.
class RegisterWindow:
    # El constructor (__init__) inicializa la ventana de registro.
    # Recibe la ventana raíz y el conector de la base de datos.
    def __init__(self, root, db):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        
        # Creamos una instancia del Controlador de Registro, pasándole esta vista y el Modelo de Usuario.
        # Esto establece la conexión entre la Vista y su Controlador.
        # El Modelo de Usuario se inicializa aquí y se pasa al controlador.
        self.controller = RegisterController(self, UserModel(db))
        
        self.image_path = None       # Almacena la ruta del archivo de imagen seleccionado (para mostrar el nombre).
        self.image_data = None       # Almacena los datos binarios de la imagen seleccionada.
        
        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.

    # Método para crear y organizar todos los widgets (campos de entrada, selectores, botones) de la ventana.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal para organizar los elementos.
        frame.grid(row=0, column=0, sticky="nsew") # Usamos grid para posicionar el marco.

        # Configuramos el sistema de grillas para que el marco se expanda correctamente.
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Etiqueta de título para la ventana de registro.
        ttk.Label(frame, text="📝 Registro Nuevo Usuario", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        self.entries = {} # Diccionario para almacenar las referencias a los campos de entrada.
        fields = ["Nombre", "Email", "Contraseña", "Celular", "Apodo"] # Lista de campos del formulario.

        # Creamos etiquetas y campos de entrada para cada campo de la lista.
        for i, field in enumerate(fields):
            ttk.Label(frame, text=f"{field}:").grid(row=i + 1, column=0, pady=5, padx=5, sticky="w")
            entry = ttk.Entry(frame, width=30)
            if field == "Contraseña":
                entry.config(show="*") # Oculta los caracteres de la contraseña.
            entry.grid(row=i + 1, column=1, pady=5, padx=5)
            self.entries[field.lower()] = entry # Guardamos la referencia al campo de entrada.

        # --- Sección de Fecha de Nacimiento ---
        # Etiqueta y selector de fecha para la fecha de nacimiento.
        dob_row = len(fields) + 1
        ttk.Label(frame, text="Fecha de Nacimiento:").grid(row=dob_row, column=0, pady=5, padx=5, sticky="w")
        # DateEntry de tkcalendar proporciona un calendario flotante para seleccionar la fecha.
        self.dob_entry = DateEntry(frame, width=27, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', top_level=self.root)
        self.dob_entry.grid(row=dob_row, column=1, pady=5, padx=5)

        # --- Sección de Carga de Imagen de Perfil ---
        image_row = len(fields) + 2
        ttk.Label(frame, text="Imagen de Perfil:").grid(row=image_row, column=0, pady=5, padx=5, sticky="w")
        
        image_frame = ttk.Frame(frame) # Marco para agrupar la etiqueta de la imagen y el botón.
        image_frame.grid(row=image_row, column=1, pady=5, padx=5, sticky="ew")
        
        self.image_label = ttk.Label(image_frame, text="Ninguna imagen seleccionada", anchor="w")
        self.image_label.pack(side="left", fill="x", expand=True)
        
        # Botón para seleccionar una imagen. Al hacer clic, llama al método 'select_image'.
        ttk.Button(image_frame, text="Seleccionar", command=self.select_image).pack(side="right")
        # --- Fin Sección de Carga de Imagen de Perfil ---

        # Botón para registrar al nuevo usuario. Al hacer clic, llama al método 'register'.
        ttk.Button(frame, text="Registrar", command=self.register).grid(row=len(fields) + 3, column=0, columnspan=2, pady=20)

    # Método para abrir un diálogo de selección de archivo y cargar la imagen de perfil.
    def select_image(self):
        # Abre un diálogo para que el usuario elija un archivo de imagen.
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen de Perfil",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.* ")]
        )
        if file_path: # Si el usuario seleccionó un archivo...
            try:
                with open(file_path, 'rb') as f: # Abrimos el archivo en modo binario de lectura.
                    self.image_data = f.read() # Leemos los datos binarios de la imagen.
                self.image_path = file_path # Guardamos la ruta del archivo (para mostrar el nombre).
                self.image_label.config(text=file_path.split('/')[-1]) # Mostramos solo el nombre del archivo.
            except Exception as e: # Capturamos cualquier error al leer la imagen.
                messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")
                self.image_data = None
                self.image_path = None
                self.image_label.config(text="Ninguna imagen seleccionada")
        else: # Si el usuario canceló la selección o no eligió archivo.
            self.image_data = None
            self.image_path = None
            self.image_label.config(text="Ninguna imagen seleccionada")

    # Método para limpiar todos los campos del formulario de registro.
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END) # Borra el contenido de cada campo de entrada.
        self.dob_entry.set_date(None) # Limpia el selector de fecha.
        self.image_data = None
        self.image_path = None
        self.image_label.config(text="Ninguna imagen seleccionada") # Restablece la etiqueta de imagen.

    # Método que se ejecuta cuando el usuario hace clic en el botón "Registrar".
    def register(self):
        # Obtenemos los datos de los campos de entrada del formulario.
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        # Creamos un diccionario con los datos del usuario a registrar.
        user_data = {
            'nombre': data['nombre'],
            'email': data['email'],
            'contraseña': data['contraseña'],
            # Obtenemos la fecha del selector y la formateamos como cadena 'YYYY-MM-DD'.
            'edad': self.dob_entry.get_date().strftime('%Y-%m-%d') if self.dob_entry.get_date() else '',
            'celular': data['celular'],
            'apodo': data['apodo'],
        }
        
        # Le pedimos al controlador que intente registrar al usuario con estos datos y la imagen.
        self.controller.register_user(user_data, self.image_data)
