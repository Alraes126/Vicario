import tkinter as tk
from tkinter import ttk
import datetime

class TransactionsWindow:
    def __init__(self, root, db, user, notebook):
        # Inicializa la ventana de transacciones
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
        # Llama a la función para cargar las transacciones del uzuario en la tabla
        self.load_transactions()

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de transacciones
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="💳 MIS TRANSACCIONES", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview para transacciones
        columns = ("ID", "Tipo", "Monto", "Fecha", "Estado")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).pack(pady=10)

    def load_transactions(self):
        # Esta función carga los datos de las transacciones en la tabla

        # Datos de ejemplo TODO: Reemplazar con datos reales de la base de datos
        dummy_transactions = [
            {'idtransaccion': 1, 'tipo': 'Depósito', 'monto_transaccion': 100.0, 'fecha_transaccion': datetime.date(2023, 10, 27), 'estado': 'Completado'},
            {'idtransaccion': 2, 'tipo': 'Retiro', 'monto_transaccion': 50.0, 'fecha_transaccion': datetime.date(2023, 10, 26), 'estado': 'Completado'},
        ]

        for trans in dummy_transactions:
            self.tree.insert("", "end", values=(
                trans['idtransaccion'],
                trans['tipo'],
                f"${trans['monto_transaccion']:.2f}",
                trans['fecha_transaccion'],
                trans['estado']
            ))

    def back_to_dashboard(self):
        # Esta función sirve para cambiar a la pestaña del panel de usuario (Dashboard)
        self.notebook.select(2) # Asume que el Dashboard es la tercera pestaña (índice 2)
