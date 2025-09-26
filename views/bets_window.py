import tkinter as tk
from tkinter import ttk
import datetime
from models.user_model import UserModel # Added import
from models.game_model import GameModel # Added import
from models.bet_model import BetModel # Added import
from controllers.bet_controller import BetController # Added import

class BetsWindow:
    def __init__(self, root, db, user_placeholder, notebook):
        # Inicializa la ventana de apuestas
        # Guarda la ventana principal (root) la conexión a la base de datos (db) 
        # el usuario (user) y el widget de pestañas (notebook)
        self.root = root
        self.db = db
        self.notebook = notebook
        self.user_model = UserModel(db) # Initialize UserModel
        self.game_model = GameModel(db) # Initialize GameModel
        self.bet_model = BetModel(db) # Initialize BetModel
        self.controller = BetController(self, self.bet_model, self.user_model, self.game_model) # Initialize Controller

        # Limpia la ventana principal de cualquier widget que existiera antes
        for widget in self.root.winfo_children():
            widget.destroy()

        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()
        # If a placeholder user is passed, set it in the controller
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)
        self.load_bets() # Load bets after setting user

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de apuestas
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="🎯 MIS APUESTAS", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("ID", "Juego", "Monto", "Resultado", "Ganancia", "Fecha")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).pack(pady=10)

    def display_bets(self, bets):
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        for bet in bets:
            self.tree.insert("", "end", values=(
                bet['idapuesta'],
                bet['nombre_juego'], # Use enhanced game name
                f"${bet['monto']:.2f}",
                bet['resultado'],
                f"${bet['ganancia']:.2f}",
                bet['fecha_apuesta']
            ))

    def load_bets(self):
        # This function now just triggers the controller to load bets
        self.controller.load_user_bets()

    def back_to_dashboard(self):
        # Esta función sirve para cambiar a la pestaña del panel de usuario (Dashboard)
        # TODO: Refresh dashboard user data before going back
        self.notebook.select(2) # Asume que el Dashboard es la tercera pestaña (índice 2)
