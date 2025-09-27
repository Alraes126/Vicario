# controllers/dashboard_controller.py
# Este archivo define el controlador para el panel de usuario (Dashboard).
# El Dashboard es la vista principal donde el usuario ve su información y opciones.

# --- Definición de la Clase DashboardController ---
# Esta clase sigue el patrón de diseño MVC (Modelo-Vista-Controlador).
# Su responsabilidad principal es gestionar la lógica del Dashboard,
# actuando como un centro de coordinación para la información del usuario.
class DashboardController:
    # El constructor (__init__) inicializa el controlador con las dependencias necesarias.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, view, user_model):
        self.view = view             # La Vista asociada a este controlador (UserDashboard).
        self.user_model = user_model # El Modelo de Usuario para interactuar con los datos del usuario.
        self.current_user = None     # Almacena los datos del usuario actualmente logueado.
        
        # Referencias a otros controladores. Se inicializan como None y se asignan más tarde.
        # Esto permite la comunicación entre diferentes partes de la aplicación (coordinación de controladores).
        self.slot_machine_controller = None
        self.bet_controller = None
        self.transaction_controller = None

    # Método para establecer el usuario actual en el controlador.
    # Se llama cuando un usuario inicia sesión o cuando los datos del usuario se actualizan.
    def set_current_user(self, user_data):
        self.current_user = user_data       # Actualizamos el usuario actual en este controlador.
        self.view.update_dashboard(user_data) # Le decimos a la Vista del Dashboard que se actualice con los nuevos datos.
        
        # --- Propagación de Datos del Usuario ---
        # Es crucial que otros controladores también sepan quién es el usuario actual.
        # Aquí, propagamos los datos del usuario a los controladores de la máquina tragamonedas, apuestas y transacciones.
        # Esto es un ejemplo de comunicación entre controladores.
        if self.slot_machine_controller:
            self.slot_machine_controller.set_current_user(user_data)
            # También pasamos referencias a los modelos y controladores de apuestas a la máquina tragamonedas.
            # Esto es necesario para que la máquina tragamonedas pueda registrar apuestas y actualizar el saldo.
            self.slot_machine_controller.bet_model = self.bet_controller.bet_model
            self.slot_machine_controller.bet_controller = self.bet_controller
        if self.bet_controller:
            self.bet_controller.set_current_user(user_data)
        if self.transaction_controller:
            self.transaction_controller.set_current_user(user_data)

    # Método para refrescar los datos del usuario desde la base de datos.
    # Se usa cuando el saldo o cualquier otra información del usuario puede haber cambiado (ej. después de un depósito).
    def refresh_user_data(self):
        if self.current_user: # Verificamos que haya un usuario logueado.
            # Obtenemos la información más reciente del usuario desde el modelo.
            updated_user = self.user_model.get_user_by_id(self.current_user['idcedula'])
            if updated_user:
                self.set_current_user(updated_user) # Si se obtienen datos, actualizamos el usuario actual.
            else:
                # Si no se pueden obtener los datos, imprimimos un error en la consola.
                print("Error: No se pudieron refrescar los datos del usuario.")