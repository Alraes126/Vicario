import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from models.user_model import UserModel
from models.transaction_model import TransactionModel
from controllers.transaction_controller import TransactionController

class TransactionsWindow:
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root
        self.db = db
        self.notebook = notebook
        self.user_model = UserModel(db)
        self.transaction_model = TransactionModel(db)
        self.controller = TransactionController(self, self.transaction_model, self.user_model)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.deposit_amount_entry = None # New
        self.payment_method_var = tk.StringVar() # New
        self.create_widgets()
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)
        self.load_transactions()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="💳 MIS TRANSACCIONES", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Deposit Section ---
        deposit_frame = ttk.LabelFrame(frame, text="Realizar Depósito", padding=10)
        deposit_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(deposit_frame, text="Monto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.deposit_amount_entry = ttk.Entry(deposit_frame, width=20)
        self.deposit_amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(deposit_frame, text="Método de Pago:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        payment_methods = ['PSE', 'transferencia de ciertos bancos']
        self.payment_method_optionmenu = ttk.OptionMenu(deposit_frame, self.payment_method_var, payment_methods[0], *payment_methods)
        self.payment_method_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(deposit_frame, text="Depositar", command=self.make_deposit_request).grid(row=2, column=0, columnspan=2, pady=10)
        # --- End Deposit Section ---

        # Treeview para transacciones
        columns = ("ID", "Tipo", "Monto", "Fecha", "Estado")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).pack(pady=10)

    def display_transactions(self, transactions):
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        for trans in transactions:
            self.tree.insert("", "end", values=(
                trans['idtransaccion'],
                trans['tipo'],
                f"${trans['monto_transaccion']:.2f}",
                trans['fecha_transaccion'],
                trans['estado']
            ))

    def load_transactions(self):
        # This function now just triggers the controller to load transactions
        self.controller.load_user_transactions()

    def make_deposit_request(self):
        # This method will call the controller
        amount_str = self.deposit_amount_entry.get()
        payment_method = self.payment_method_var.get()
        self.controller.request_deposit(amount_str, payment_method)

    def back_to_dashboard(self):
        # TODO: Refresh dashboard user data before going back
        self.notebook.select(2)