# controllers/transaction_controller.py
from tkinter import messagebox
from decimal import Decimal # Added import

class TransactionController:
    def __init__(self, view, transaction_model, user_model):
        self.view = view
        self.transaction_model = transaction_model
        self.user_model = user_model
        self.current_user = None
        self.dashboard_controller = None # New: to refresh dashboard after deposit

    def set_current_user(self, user_data):
        self.current_user = user_data
        self.load_user_transactions()

    def load_user_transactions(self):
        if self.current_user:
            transactions = self.transaction_model.get_transactions_by_user(self.current_user['idcedula'])
            self.view.display_transactions(transactions)

    def request_deposit(self, amount_str, payment_method):
        if not self.current_user:
            messagebox.showerror("Error", "No hay usuario logueado para realizar un depósito.")
            return

        try:
            amount = Decimal(amount_str) # Changed to Decimal
            if amount <= 0:
                messagebox.showerror("Error", "El monto del depósito debe ser positivo.")
                return
        except Exception: # Catching a broader exception for Decimal conversion
            messagebox.showerror("Error", "Monto inválido. Introduce un número válido.")
            return

        # Create transaction record
        transaction_data = {
            'idcedula': self.current_user['idcedula'],
            'tipo': 'deposito',
            'metododepago': payment_method,
            'monto_transaccion': amount,
            'estado': 'completado' # Assuming deposits are instantly completed
        }
        transaction_success = self.transaction_model.create_transaction(transaction_data)

        if transaction_success:
            # Update user balance
            new_balance = self.current_user['saldo'] + amount # Now both are Decimal
            user_balance_updated = self.user_model.update_user_balance(self.current_user['idcedula'], new_balance)

            if user_balance_updated:
                self.current_user['saldo'] = new_balance # Update local user data
                messagebox.showinfo("Éxito", f"Depósito de ${amount:.2f} realizado con éxito. Nuevo saldo: ${new_balance:.2f}")
                self.view.load_transactions() # Refresh transaction list
                if self.dashboard_controller: # Refresh dashboard balance
                    self.dashboard_controller.refresh_user_data()
            else:
                messagebox.showerror("Error", "Depósito registrado, pero no se pudo actualizar el saldo del usuario.")
        else:
            messagebox.showerror("Error", "No se pudo registrar el depósito.")
