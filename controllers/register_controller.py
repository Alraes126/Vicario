# controllers/register_controller.py
from tkinter import messagebox

class RegisterController:
    def __init__(self, view, user_model):
        self.view = view
        self.user_model = user_model

    def register_user(self, user_data, image_data):
        # Valida que todos los campos estén completos
        if not all(user_data.values()):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False

        # Valida que la edad sea un número y que el usuario sea mayor de 18 años
        try:
            edad = int(user_data['edad'])
            if edad < 18:
                messagebox.showerror("Error", "Debes ser mayor de 18 años")
                return False
        except ValueError:
            messagebox.showerror("Error", "Edad inválida")
            return False

        # Call UserModel to create the user
        success = self.user_model.create_user(user_data, image_data)

        if success:
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente!")
            # Clear form fields after successful registration
            self.view.clear_form() # Assuming view has a clear_form method
            return True
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario. Inténtalo de nuevo.")
            return False
