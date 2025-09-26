import tkinter as tk
from tkinter import ttk
from models.user_model import UserModel
from controllers.dashboard_controller import DashboardController
from PIL import Image, ImageTk # Added imports
import io # Added import

class UserDashboard:
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root
        self.db = db
        self.notebook = notebook
        self.user_model = UserModel(db)
        self.controller = DashboardController(self, self.user_model)
        self.user_data = None

        self.welcome_label = None
        self.balance_label = None
        self.email_label = None # New label
        self.age_label = None # New label
        self.profile_image_label = None # New label for image
        self.tk_image = None # To keep a reference to the image

        self.create_widgets()
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Profile Image
        self.profile_image_label = ttk.Label(frame)
        self.profile_image_label.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ne") # Positioned top-right

        self.welcome_label = ttk.Label(frame, text="👋 Bienvenido", font=("Arial", 16, "bold"))
        self.welcome_label.grid(row=0, column=0, pady=10, sticky="w")

        self.balance_label = ttk.Label(frame, text="Saldo: $0.00", font=("Arial", 14))
        self.balance_label.grid(row=1, column=0, pady=5, sticky="w")

        self.email_label = ttk.Label(frame, text="Email: ", font=("Arial", 10)) # New label
        self.email_label.grid(row=2, column=0, pady=2, sticky="w")

        self.age_label = ttk.Label(frame, text="Edad: ", font=("Arial", 10)) # New label
        self.age_label.grid(row=3, column=0, pady=2, sticky="w")

        ttk.Label(frame, text="🎰 ¿Qué quieres hacer hoy?", font=("Arial", 12)).grid(row=4, column=0, pady=20, sticky="w") # Adjusted row

        ttk.Button(frame, text="Jugar Tragamonedas", command=self.open_slots, width=20).grid(row=5, column=0, pady=5, sticky="w") # Adjusted row
        ttk.Button(frame, text="Ver mis Transacciones", command=self.open_transactions, width=20).grid(row=6, column=0, pady=5, sticky="w") # Adjusted row
        ttk.Button(frame, text="Ver mis Apuestas", command=self.open_bets, width=20).grid(row=7, column=0, pady=5, sticky="w") # Adjusted row

    def update_dashboard(self, user_data):
        self.user_data = user_data
        if self.user_data:
            self.welcome_label.config(text=f"👋 Bienvenido {self.user_data['nombre']}")
            self.balance_label.config(text=f"Saldo: ${self.user_data['saldo']:.2f}")
            self.email_label.config(text=f"Email: {self.user_data['correo']}") # Update new label
            self.age_label.config(text=f"Edad: {self.user_data['edad']}") # Update new label

            # Display profile image
            if self.user_data['ruta_imagen']:
                try:
                    img = Image.open(io.BytesIO(self.user_data['ruta_imagen']))
                    img.thumbnail((100, 100), Image.Resampling.LANCZOS) # Resize for display
                    self.tk_image = ImageTk.PhotoImage(img) # Keep reference!
                    self.profile_image_label.config(image=self.tk_image)
                except Exception as e:
                    print(f"Error al cargar la imagen de perfil: {e}")
                    self.profile_image_label.config(image='') # Clear image on error
            else:
                self.profile_image_label.config(image='') # Clear image if no data
        else:
            self.welcome_label.config(text="👋 Bienvenido")
            self.balance_label.config(text="Saldo: $0.00")
            self.email_label.config(text="Email: ")
            self.age_label.config(text="Edad: ")
            self.profile_image_label.config(image='')

    def open_slots(self):
        # Esta función sirve para cambiar a la pestaña de la tragamonedas
        self.notebook.select(3) # Asume que la Tragamonedas es la cuarta pestaña (índice 3)

    def open_transactions(self):
        # Esta función sirve para cambiar a la pestaña de transacciones
        self.notebook.select(5) # Asume que la de Transacciones es la sexta pestaña (índice 5)

    def open_bets(self):
        # Esta función sirve para cambiar a la pestaña de apuestas
        self.notebook.select(4) # Asume que la de Apuestas es la quinta pestaña (índice 4)
