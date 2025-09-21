# Importa las bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
# Importa las clases de las diferentes ventanas de la interfaz de usuario
from UI.login_window import LoginWindow
from UI.register_window import RegisterWindow
from UI.user_dashboard import UserDashboard
from UI.slot_machine import SlotMachine
from UI.bets_window import BetsWindow
from UI.transaction_window import TransactionsWindow

# Función principal que se ejecuta al iniciar la aplicación
def main():
    # Crea la ventana principal de la aplicación
    root = tk.Tk()
    root.title("Casino Vicario")  # Establece el título de la ventana
    root.geometry("800x600")  # Establece el tamaño de la ventana

    # Crea un widget de pestañas (Notebook) para organizar las diferentes ventanas
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    # Crea un objeto de base de datos ficticio por ahora
    db_placeholder = None
    # Crea un usuario ficticio por ahora
    user_placeholder = {'idcedula': 1, 'nombre': 'Test User', 'saldo': 1000}

    # Crea los marcos (frames) para cada una de las pestañas
    login_frame = ttk.Frame(notebook, width=400, height=280)
    register_frame = ttk.Frame(notebook, width=400, height=280)
    dashboard_frame = ttk.Frame(notebook, width=400, height=280)
    slot_machine_frame = ttk.Frame(notebook, width=400, height=280)
    bets_frame = ttk.Frame(notebook, width=400, height=280)
    transactions_frame = ttk.Frame(notebook, width=400, height=280)

    # Empaqueta los marcos para que se muestren correctamente
    login_frame.pack(fill="both", expand=True)
    register_frame.pack(fill="both", expand=True)
    dashboard_frame.pack(fill="both", expand=True)
    slot_machine_frame.pack(fill="both", expand=True)
    bets_frame.pack(fill="both", expand=True)
    transactions_frame.pack(fill="both", expand=True)

    # Agrega los marcos al widget de pestañas con sus respectivos títulos
    notebook.add(login_frame, text="Login")
    notebook.add(register_frame, text="Register")
    notebook.add(dashboard_frame, text="Dashboard")
    notebook.add(slot_machine_frame, text="Slot Machine")
    notebook.add(bets_frame, text="Bets")
    notebook.add(transactions_frame, text="Transactions")

    # Rellena cada pestaña con su contenido correspondiente
    LoginWindow(login_frame, db_placeholder, notebook)
    RegisterWindow(register_frame, db_placeholder)
    UserDashboard(dashboard_frame, db_placeholder, user_placeholder, notebook)
    SlotMachine(slot_machine_frame, db_placeholder, user_placeholder, notebook)
    BetsWindow(bets_frame, db_placeholder, user_placeholder, notebook)
    TransactionsWindow(transactions_frame, db_placeholder, user_placeholder, notebook)

    # Inicia el bucle principal de la aplicación para que la ventana sea interactiva
    root.mainloop()


# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    # Llama a la función principal para iniciar la aplicación
    main()
