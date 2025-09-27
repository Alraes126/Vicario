import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk # Importamos ttk para widgets con estilos modernos.

# Importamos los Modelos y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from controllers.dashboard_controller import DashboardController

# Importamos clases de la biblioteca Pillow (PIL) para manipulación de imágenes.
from PIL import Image, ImageTk, ImageDraw
import io # Importamos io para trabajar con datos binarios de la imagen en memoria.

# --- Definición de la Clase UserDashboard ---
# Esta clase representa la Vista (GUI) para el panel de usuario (Dashboard).
# Es responsable de cómo se ve la información del usuario y las opciones disponibles.
class UserDashboard:
    # El constructor (__init__) inicializa el Dashboard.
    # Recibe la ventana raíz, el conector de la base de datos, un placeholder de usuario y el widget de pestañas.
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        self.notebook = notebook     # El widget de pestañas (ttk.Notebook) para cambiar entre vistas.
        
        # Inicializamos el Modelo de Usuario.
        self.user_model = UserModel(db)
        # Creamos una instancia del Controlador del Dashboard, pasándole esta vista y el modelo.
        # Esto establece la conexión entre la Vista y su Controlador.
        self.controller = DashboardController(self, self.user_model)
        self.user_data = None        # Almacena los datos del usuario actualmente logueado.

        # Atributos para los widgets que se actualizarán dinámicamente.
        self.welcome_label = None
        self.balance_label = None
        self.email_label = None
        self.age_label = None
        self.profile_image_label = None
        self.tk_image = None         # Referencia a la imagen de perfil del usuario (PhotoImage).
        self.placeholder_tk_image = None # Referencia a la imagen de placeholder.
        
        self._create_placeholder_image() # Llamamos a un método para crear la imagen de placeholder.

        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.
        
        # Si se pasa un usuario al inicializar, lo establecemos en el controlador.
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)

    # Método privado para crear la imagen de placeholder.
    # Intenta cargar una imagen desde 'assets/placeholder.png'; si falla, crea una por defecto.
    def _create_placeholder_image(self):
        placeholder_path = "assets/placeholder.png" # Ruta esperada para la imagen de placeholder.
        try:
            img = Image.open(placeholder_path) # Intentamos abrir la imagen.
            img.thumbnail((100, 100), Image.Resampling.LANCZOS) # Redimensionamos la imagen.
            self.placeholder_tk_image = ImageTk.PhotoImage(img) # Convertimos a formato PhotoImage para Tkinter.
        except FileNotFoundError:
            print(f"WARNING: Placeholder image not found at {placeholder_path}. Using default.")
            # Si el archivo no se encuentra, creamos una imagen de placeholder por defecto.
            img = Image.new('RGB', (100, 100), color = 'lightgray')
            d = ImageDraw.Draw(img)
            d.text((10,40), "No Photo", fill=(0,0,0))
            self.placeholder_tk_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"WARNING: Error loading placeholder image: {e}. Using default.")
            # Si ocurre otro error al cargar la imagen, también usamos la por defecto.
            img = Image.new('RGB', (100, 100), color = 'lightgray')
            d = ImageDraw.Draw(img)
            d.text((10,40), "No Photo", fill=(0,0,0))
            self.placeholder_tk_image = ImageTk.PhotoImage(img)

    # Método para crear y organizar todos los widgets del Dashboard.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal.
        frame.grid(row=0, column=0, sticky="nsew") # Usamos grid para posicionar el marco.
        
        # Configuramos el sistema de grillas para que el marco se expanda correctamente.
        self.root.grid_row_configure(0, weight=1)
        self.root.grid_column_configure(0, weight=1)
        frame.grid_column_configure(0, weight=1)

        # Etiqueta para la imagen de perfil del usuario.
        self.profile_image_label = ttk.Label(frame)
        self.profile_image_label.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ne") # Posicionada arriba a la derecha.

        # Etiqueta de bienvenida al usuario.
        self.welcome_label = ttk.Label(frame, text="👋 Bienvenido", font=("Arial", 16, "bold"))
        self.welcome_label.grid(row=0, column=0, pady=10, sticky="w")

        # Etiqueta para mostrar el saldo del usuario.
        self.balance_label = ttk.Label(frame, text="Saldo: $0.00", font=("Arial", 14))
        self.balance_label.grid(row=1, column=0, pady=5, sticky="w")

        # Etiqueta para mostrar el email del usuario.
        self.email_label = ttk.Label(frame, text="Email: ", font=("Arial", 10))
        self.email_label.grid(row=2, column=0, pady=2, sticky="w")

        # Etiqueta para mostrar la edad del usuario.
        self.age_label = ttk.Label(frame, text="Edad: ", font=("Arial", 10))
        self.age_label.grid(row=3, column=0, pady=2, sticky="w")

        # Etiqueta con una pregunta para el usuario.
        ttk.Label(frame, text="🎰 ¿Qué quieres hacer hoy?", font=("Arial", 12)).grid(row=4, column=0, pady=20, sticky="w")

        # Botones para navegar a otras secciones de la aplicación.
        ttk.Button(frame, text="Jugar Tragamonedas", command=self.open_slots, width=20).grid(row=5, column=0, pady=5, sticky="w")
        ttk.Button(frame, text="Ver mis Transacciones", command=self.open_transactions, width=20).grid(row=6, column=0, pady=5, sticky="w")
        ttk.Button(frame, text="Ver mis Apuestas", command=self.open_bets, width=20).grid(row=7, column=0, pady=5, sticky="w")

    # Método para actualizar la información mostrada en el Dashboard.
    # Se llama cuando los datos del usuario cambian (ej. login, actualización de saldo).
    def update_dashboard(self, user_data):
        self.user_data = user_data # Almacenamos los datos del usuario.
        if self.user_data: # Si hay datos de usuario...
            # Actualizamos las etiquetas con la información del usuario.
            self.welcome_label.config(text=f"👋 Bienvenido {self.user_data['apodo']}")
            self.balance_label.config(text=f"Saldo: ${self.user_data['saldo']:.2f}")
            self.email_label.config(text=f"Email: {self.user_data['correo']}")
            self.age_label.config(text=f"Edad: {self.user_data['edad']}")

            # --- Mostrar Imagen de Perfil ---
            if self.user_data['ruta_imagen']: # Si el usuario tiene una imagen de perfil...
                print(f"DEBUG: ruta_imagen is not empty. Type: {type(self.user_data['ruta_imagen'])}, Length: {len(self.user_data['ruta_imagen']) if self.user_data['ruta_imagen'] else 'None'}")
                try:
                    # Abrimos la imagen desde los datos binarios.
                    img = Image.open(io.BytesIO(self.user_data['ruta_imagen']))
                    img.thumbnail((100, 100), Image.Resampling.LANCZOS) # Redimensionamos para mostrar.
                    self.tk_image = ImageTk.PhotoImage(img) # Convertimos a PhotoImage.
                    self.profile_image_label.config(image=self.tk_image) # Mostramos la imagen.
                except Exception as e:
                    print(f"Error al cargar la imagen de perfil: {e}")
                    self.profile_image_label.config(image=self.placeholder_tk_image) # Si hay error, mostramos el placeholder.
            else: # Si el usuario no tiene imagen de perfil...
                self.profile_image_label.config(image=self.placeholder_tk_image) # Mostramos el placeholder.
        else: # Si no hay datos de usuario (ej. no logueado)...
            # Restablecemos las etiquetas y mostramos el placeholder.
            self.welcome_label.config(text="👋 Bienvenido")
            self.balance_label.config(text="Saldo: $0.00")
            self.email_label.config(text="Email: ")
            self.age_label.config(text="Edad: ")
            self.profile_image_label.config(image=self.placeholder_tk_image)

    # Método para cambiar a la pestaña de la máquina tragamonedas.
    def open_slots(self):
        self.notebook.select(3) # Seleccionamos la cuarta pestaña (índice 3).

    # Método para cambiar a la pestaña de transacciones.
    def open_transactions(self):
        self.notebook.select(5) # Seleccionamos la sexta pestaña (índice 5).

    # Método para cambiar a la pestaña de apuestas.
    def open_bets(self):
        self.notebook.select(4) # Seleccionamos la quinta pestaña (índice 4).