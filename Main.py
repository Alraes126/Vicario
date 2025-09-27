# main.py
# Este es el archivo principal que inicia nuestra aplicación de casino.
# Aquí configuramos la ventana principal, las pestañas y conectamos todas las partes (modelos, vistas, controladores).

# --- Importación de Bibliotecas ---
# Importamos 'tkinter' para crear la interfaz gráfica de usuario (GUI).
import tkinter as tk
# Importamos 'ttk' (Themed Tkinter) para usar widgets con estilos modernos.
from tkinter import ttk

# Importamos las clases de las Vistas (la parte de la GUI que el usuario ve).
# Cada vista representa una ventana o sección diferente de la aplicación.
from views.login_window import LoginWindow
from views.register_window import RegisterWindow
from views.user_dashboard import UserDashboard
from views.slot_machine import SlotMachine
from views.bets_window import BetsWindow
from views.transaction_window import TransactionsWindow

# Importamos las clases de los Modelos (la parte que gestiona los datos y la lógica de negocio).
# Los modelos interactúan con la base de datos.
from models.Database.database_manager import DatabaseConnector # Para conectar con la base de datos
from models.user_model import UserModel         # Gestiona los datos de los usuarios
from models.game_model import GameModel         # Gestiona los datos de los juegos
from models.bet_model import BetModel           # Gestiona los datos de las apuestas
from models.transaction_model import TransactionModel # Gestiona los datos de las transacciones

# Importamos las clases de los Controladores (la parte que maneja la interacción entre Vistas y Modelos).
# Los controladores responden a las acciones del usuario y actualizan la vista o el modelo.
from controllers.login_controller import LoginController
from controllers.register_controller import RegisterController
from controllers.dashboard_controller import DashboardController
from controllers.slot_machine_controller import SlotMachineController
from controllers.bet_controller import BetController
from controllers.transaction_controller import TransactionController


# --- Función Principal de la Aplicación ---
# Esta función 'main' es el punto de entrada de nuestra aplicación.
# Aquí se inicializan todos los componentes.
def main():
    # Creamos la ventana principal de la aplicación.
    # 'tk.Tk()' es la clase base para todas las ventanas Tkinter.
    root = tk.Tk()
    root.title("Casino Vicario") # Establecemos el título de la ventana.
    root.geometry("800x600")     # Definimos el tamaño inicial de la ventana (ancho x alto).

    # Creamos un 'notebook' (un widget de pestañas) para organizar las diferentes secciones de la app.
    # 'ttk.Notebook' permite cambiar entre diferentes vistas fácilmente.
    notebook = ttk.Notebook(root)
    # Empaquetamos el notebook para que ocupe todo el espacio disponible en la ventana principal.
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    # --- Inicialización de la Base de Datos ---
    # Creamos una instancia de DatabaseConnector para manejar la conexión a la base de datos.
    # Este es un ejemplo del patrón Singleton o una clase de utilidad para la gestión de recursos.
    db_connector = DatabaseConnector()

    # --- Inicialización de los Modelos ---
    # Creamos instancias de cada modelo, pasándoles el conector de la base de datos.
    # Esto es un ejemplo de Inyección de Dependencias, donde los modelos 'dependen' del conector DB.
    user_model = UserModel(db_connector)
    game_model = GameModel(db_connector)
    bet_model = BetModel(db_connector)
    transaction_model = TransactionModel(db_connector)

    # --- Creación de Marcos (Frames) para cada Pestaña ---
    # Cada pestaña del notebook tendrá su propio 'frame' (marco) para contener sus widgets.
    # 'ttk.Frame' es un contenedor que ayuda a organizar la GUI.
    login_frame = ttk.Frame(notebook, width=400, height=280)
    register_frame = ttk.Frame(notebook, width=400, height=280)
    dashboard_frame = ttk.Frame(notebook, width=400, height=280)
    slot_machine_frame = ttk.Frame(notebook, width=400, height=280)
    bets_frame = ttk.Frame(notebook, width=400, height=280)
    transactions_frame = ttk.Frame(notebook, width=400, height=280)

    # Empaquetamos cada frame para que ocupe todo el espacio de su pestaña.
    login_frame.pack(fill="both", expand=True)
    register_frame.pack(fill="both", expand=True)
    dashboard_frame.pack(fill="both", expand=True)
    slot_machine_frame.pack(fill="both", expand=True)
    bets_frame.pack(fill="both", expand=True)
    transactions_frame.pack(fill="both", expand=True)

    # --- Añadir Marcos como Pestañas al Notebook ---
    # Asignamos cada frame a una pestaña en el notebook con su texto correspondiente.
    notebook.add(login_frame, text="Login")
    notebook.add(register_frame, text="Register")
    notebook.add(dashboard_frame, text="Dashboard")
    notebook.add(slot_machine_frame, text="Slot Machine")
    notebook.add(bets_frame, text="Bets")
    notebook.add(transactions_frame, text="Transactions")

    # --- Inicialización de Vistas y Controladores (Patrón MVC) ---
    # Aquí aplicamos el patrón Modelo-Vista-Controlador (MVC).
    # Cada Vista (GUI) tiene un Controlador asociado que maneja su lógica.

    # Inicializamos el Dashboard primero porque otros controladores necesitan su referencia.
    dashboard_view = UserDashboard(dashboard_frame, db_connector, None, notebook)
    dashboard_controller = dashboard_view.controller # Obtenemos la instancia del controlador del dashboard.

    # Inicializamos la Vista y el Controlador de la Máquina Tragamonedas.
    slot_machine_view = SlotMachine(slot_machine_frame, db_connector, None, notebook)
    slot_machine_controller = slot_machine_view.controller

    # Inicializamos la Vista y el Controlador de Apuestas.
    bets_view = BetsWindow(bets_frame, db_connector, None, notebook)
    bet_controller = bets_view.controller

    # Inicializamos la Vista y el Controlador de Transacciones.
    transactions_view = TransactionsWindow(transactions_frame, db_connector, None, notebook)
    transaction_controller = transactions_view.controller
    # Pasamos el controlador del dashboard al controlador de transacciones para que pueda actualizar el saldo.
    transaction_controller.dashboard_controller = dashboard_controller

    # --- Propagación de Controladores ---
    # Los controladores a menudo necesitan comunicarse entre sí.
    # Aquí, el controlador del dashboard recibe referencias a otros controladores.
    # Esto permite que el dashboard, por ejemplo, actualice el saldo en la máquina tragamonedas.
    dashboard_controller.slot_machine_controller = slot_machine_controller
    dashboard_controller.bet_controller = bet_controller
    dashboard_controller.transaction_controller = transaction_controller

    # El controlador de la máquina tragamonedas también necesita una referencia al controlador del dashboard.
    slot_machine_view.controller.dashboard_controller = dashboard_controller

    # Inicializamos la Vista y el Controlador de Login.
    login_view = LoginWindow(login_frame, db_connector, notebook)
    # El controlador de login necesita referencias a otros controladores para propagar la información del usuario logueado.
    login_view.controller.dashboard_controller = dashboard_controller
    login_view.controller.slot_machine_controller = slot_machine_controller
    login_view.controller.bet_controller = bet_controller
    login_view.controller.transaction_controller = transaction_controller

    # Inicializamos la Vista y el Controlador de Registro.
    register_view = RegisterWindow(register_frame, db_connector)

    # --- Bucle Principal de la GUI ---
    # 'root.mainloop()' inicia el bucle de eventos de Tkinter.
    # La aplicación permanecerá abierta y responderá a las interacciones del usuario hasta que se cierre la ventana.
    root.mainloop()

# --- Ejecución del Script ---
# Esta condición asegura que 'main()' solo se llame cuando el script se ejecuta directamente,
# no cuando se importa como un módulo en otro script.
if __name__ == "__main__":
    main()