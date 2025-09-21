import tkinter as tk
from tkinter import ttk
import datetime

class BetsWindow:
    def __init__(self, root, db, user, notebook):
        # Inicializa la ventana de apuestas
        # Guarda la ventana principal (root) la conexión a la base de datos (db) 
        # el usuario (user) y el widget de pestañas (notebook)
        self.root = root
        self.db = db
        self.user = user
        self.notebook = notebook

        # Limpia la ventana principal de cualquier widget que existiera antes
        for widget in self.root.winfo_children():
            widget.destroy()

        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()
        # Llama a la funsion para cargar las apuestas del usuario en la tabla
        self.load_bets()

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

    def load_bets(self):
        # Esta función carga los datos de las apuestas en la tabla
        
        # Datos de ejemplo TODO: Reemplazar con datos reales de la base de datos
        dummy_bets = [
            {'idapuesta': 1, 'juego': 'Tragamonedas', 'monto': 10.0, 'resultado': 'Ganó', 'ganancia': 20.0, 'fecha_apuesta': datetime.date(2023, 10, 27)},
            {'idapuesta': 2, 'juego': 'Tragamonedas', 'monto': 5.0, 'resultado': 'Perdió', 'ganancia': 0.0, 'fecha_apuesta': datetime.date(2023, 10, 26)},
        ]

        # Inserta los datos de ejemplo en la tabla
        for bet in dummy_bets:
            self.tree.insert("", "end", values=(
                bet['idapuesta'],
                bet['juego'],
                f"${bet['monto']:.2f}",
                bet['resultado'],
                f"${bet['ganancia']:.2f}",
                bet['fecha_apuesta']
            ))

    def back_to_dashboard(self):
        # Esta función sirve para cambiar a la pestaña del panel de usuario (Dashboard)
        self.notebook.select(2) # Asume que el Dashboard es la tercera pestaña (índice 2)