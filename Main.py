# main.py
# Este es el archivo principal que inicia nuestra aplicación de casino.
# Aquí configuramos la ventana principal, las pestañas y conectamos todas las partes (modelos, vistas, controladores).

# --- Importación de Bibliotecas ---
import tkinter as tk
from tkinter import ttk
import sv_ttk  # <--- 1. IMPORTAMOS LA LIBRERÍA DE TEMAS

# Importamos las clases de las Vistas
from views.login_window import LoginWindow
from views.register_window import RegisterWindow
from views.user_dashboard import UserDashboard
from views.slot_machine import SlotMachine
from views.bets_window import BetsWindow
from views.transaction_window import TransactionsWindow

# Importamos las clases de los Modelos
from models.Database.database_manager import DatabaseConnector
from models.user_model import UserModel
from models.game_model import GameModel
from models.bet_model import BetModel
from models.transaction_model import TransactionModel

# Importamos las clases de los Controladores
from controllers.login_controller import LoginController
from controllers.register_controller import RegisterController
from controllers.dashboard_controller import DashboardController
from controllers.slot_machine_controller import SlotMachineController
from controllers.bet_controller import BetController
from controllers.transaction_controller import TransactionController


# --- Función Principal de la Aplicación ---
def main():
    root = tk.Tk()
    root.title("Casino Vicario")
    root.geometry("800x600")

    # --- 2. CONFIGURACIÓN DE TEMAS ---
    # Creamos un menú principal en la ventana raíz
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Creamos un menú desplegable llamado "Tema"
    theme_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tema", menu=theme_menu)

    # Añadimos las opciones para cambiar de tema
    # Usamos radiobuttons para que solo uno pueda estar seleccionado
    theme_var = tk.StringVar(value="light") # Variable para controlar el tema actual

    def set_theme():
        if theme_var.get() == "light":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")

    theme_menu.add_radiobutton(label="Claro", variable=theme_var, value="light", command=set_theme)
    theme_menu.add_radiobutton(label="Oscuro", variable=theme_var, value="dark", command=set_theme)

    # Establecemos el tema inicial al arrancar la aplicación
    sv_ttk.set_theme("light")
    # --- FIN DE CONFIGURACIÓN DE TEMAS ---

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    db_connector = DatabaseConnector()

    user_model = UserModel(db_connector)
    game_model = GameModel(db_connector)
    bet_model = BetModel(db_connector)
    transaction_model = TransactionModel(db_connector)

    login_frame = ttk.Frame(notebook, width=400, height=280)
    register_frame = ttk.Frame(notebook, width=400, height=280)
    dashboard_frame = ttk.Frame(notebook, width=400, height=280)
    slot_machine_frame = ttk.Frame(notebook, width=400, height=280)
    bets_frame = ttk.Frame(notebook, width=400, height=280)
    transactions_frame = ttk.Frame(notebook, width=400, height=280)

    login_frame.pack(fill="both", expand=True)
    register_frame.pack(fill="both", expand=True)
    dashboard_frame.pack(fill="both", expand=True)
    slot_machine_frame.pack(fill="both", expand=True)
    bets_frame.pack(fill="both", expand=True)
    transactions_frame.pack(fill="both", expand=True)

    notebook.add(login_frame, text="Login")
    notebook.add(register_frame, text="Register")
    notebook.add(dashboard_frame, text="Dashboard")
    notebook.add(slot_machine_frame, text="Slot Machine")
    notebook.add(bets_frame, text="Bets")
    notebook.add(transactions_frame, text="Transactions")

    dashboard_view = UserDashboard(dashboard_frame, db_connector, None, notebook)
    dashboard_controller = dashboard_view.controller

    slot_machine_view = SlotMachine(slot_machine_frame, db_connector, None, notebook)
    slot_machine_controller = slot_machine_view.controller

    bets_view = BetsWindow(bets_frame, db_connector, None, notebook)
    bet_controller = bets_view.controller

    transactions_view = TransactionsWindow(transactions_frame, db_connector, None, notebook)
    transaction_controller = transactions_view.controller
    transaction_controller.dashboard_controller = dashboard_controller

    dashboard_controller.slot_machine_controller = slot_machine_controller
    dashboard_controller.bet_controller = bet_controller
    dashboard_controller.transaction_controller = transaction_controller

    slot_machine_view.controller.dashboard_controller = dashboard_controller

    login_view = LoginWindow(login_frame, db_connector, notebook)
    login_view.controller.dashboard_controller = dashboard_controller
    login_view.controller.slot_machine_controller = slot_machine_controller
    login_view.controller.bet_controller = bet_controller
    login_view.controller.transaction_controller = transaction_controller

    register_view = RegisterWindow(register_frame, db_connector)

    root.mainloop()

if __name__ == "__main__":
    main()
