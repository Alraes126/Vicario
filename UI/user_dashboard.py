import tkinter as tk
from tkinter import ttk

class UserDashboard:
    def __init__(self, root, db, user, notebook):
        # Inicializa el panel de usuario (Dashboard)
        # Guarda la ventana principal (root) la conexión a la base de datos (db)
        # el usuario (user) y el widget de pestañas (notebook)
        self.root = root
        self.db = db
        self.user = user
        self.notebook = notebook
        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()

    def create_widgets(self):
        # Esta función crea todos los widgets del panel de usuario

        # Crea un marco (frame) principal para organizar los widgets
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configura el sistema de grillas (grid) para que se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Aquí se crea la etiqueta de bienvenida para el usuario
        ttk.Label(frame, text=f"👋 Bienvenido {self.user['nombre']}",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Aquí se crea la etiqueta para mostrar el saldo del usuario
        ttk.Label(frame, text=f"Saldo: ${self.user['saldo']:.2f}",
                  font=("Arial", 14)).grid(row=1, column=0, pady=5)

        # Aquí se crea una etiqueta de texto como subtítulo
        ttk.Label(frame, text="🎰 ¿Qué quieres hacer hoy?",
                  font=("Arial", 12)).grid(row=2, column=0, pady=20)

        # Aquí se crea el botón para ir a la ventana de la tragamonedas
        ttk.Button(frame, text="Jugar Tragamonedas",
                   command=self.open_slots, width=20).grid(row=3, column=0, pady=5)
        # Aquí se crea el botón para ver las transacciones del usuario
        ttk.Button(frame, text="Ver mis Transacciones",
                   command=self.open_transactions, width=20).grid(row=4, column=0, pady=5)
        # Aquí se crea el botón para ver las apuestas del usuario
        ttk.Button(frame, text="Ver mis Apuestas",
                   command=self.open_bets, width=20).grid(row=5, column=0, pady=5)

    def open_slots(self):
        # Esta función sirve para cambiar a la pestaña de la tragamonedas
        self.notebook.select(3) # Asume que la Tragamonedas es la cuarta pestaña (índice 3)

    def open_transactions(self):
        # Esta función sirve para cambiar a la pestaña de transacciones
        self.notebook.select(5) # Asume que la de Transacciones es la sexta pestaña (índice 5)

    def open_bets(self):
        # Esta función sirve para cambiar a la pestaña de apuestas
        self.notebook.select(4) # Asume que la de Apuestas es la quinta pestaña (índice 4)