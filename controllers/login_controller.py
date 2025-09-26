# controllers/login_controller.py
from tkinter import messagebox

class LoginController:
    def __init__(self, view, user_model):
        self.view = view
        self.user_model = user_model
        self.dashboard_controller = None
        self.slot_machine_controller = None # New
        self.bet_controller = None # New
        self.transaction_controller = None # New

    def login_user(self, email, password):
        if not email or not password:
            messagebox.showerror("Error", "Email y contraseña son requeridos.")
            return False

        user = self.user_model.get_user_by_email_and_password(email, password)

        if user:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {user['nombre']}!")
            
            # Inform all relevant controllers about the logged-in user
            if self.dashboard_controller:
                self.dashboard_controller.set_current_user(user)
            if self.slot_machine_controller:
                self.slot_machine_controller.set_current_user(user)
            if self.bet_controller:
                self.bet_controller.set_current_user(user)
            if self.transaction_controller:
                self.transaction_controller.set_current_user(user)

            self.view.on_login_success(user) # Notify view of successful login
            return True
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos.")
            return False
