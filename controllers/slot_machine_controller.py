# controllers/slot_machine_controller.py
# Este archivo define el controlador para la lógica de la máquina tragamonedas.
# Un controlador gestiona la interacción del usuario con la vista de la máquina tragamonedas
# y coordina con los modelos de usuario y apuestas para simular el juego.

# --- Importación de Bibliotecas ---
import random # Importamos 'random' para generar resultados aleatorios en la máquina tragamonedas.
from tkinter import messagebox # Para mostrar mensajes emergentes al usuario.
from decimal import Decimal # Importamos 'Decimal' para manejar cálculos monetarios con precisión,
                            # evitando problemas de punto flotante que pueden ocurrir con 'float'.

# --- Definición de la Clase SlotMachineController ---
# Esta clase es un ejemplo del patrón de diseño MVC (Modelo-Vista-Controlador).
# Su responsabilidad es manejar la lógica del juego de la máquina tragamonedas.
class SlotMachineController:
    # El constructor (__init__) inicializa el controlador con las dependencias necesarias.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, view, game_model, user_model):
        self.view = view             # La Vista asociada a este controlador (SlotMachine).
        self.game_model = game_model # El Modelo de Juego para obtener información sobre los juegos.
        self.user_model = user_model # El Modelo de Usuario para interactuar con los datos del usuario (saldo).
        self.current_user = None     # Almacena los datos del usuario actualmente logueado.
        
        # Referencias a otros modelos y controladores que se asignan más tarde.
        # Esto permite la comunicación y coordinación entre diferentes partes de la aplicación.
        self.bet_model = None
        self.bet_controller = None
        self.dashboard_controller = None

    # Método para establecer el usuario actual en el controlador.
    # Se llama cuando un usuario inicia sesión o cuando los datos del usuario se actualizan.
    def set_current_user(self, user_data):
        self.current_user = user_data       # Actualizamos el usuario actual en este controlador.
        self.view.update_saldo(user_data['saldo']) # Le decimos a la Vista que actualice el saldo mostrado.

    # Método principal para simular una jugada en la máquina tragamonedas.
    # Recibe el monto de la apuesta como un número flotante.
    def play_slot_machine(self, bet_amount_float):
        if not self.current_user: # Verificamos que haya un usuario logueado.
            messagebox.showerror("Error", "No hay usuario logueado.")
            return

        # --- Validación y Conversión de la Apuesta ---
        try:
            # Convertimos el monto de la apuesta a tipo Decimal para cálculos precisos.
            bet_amount = Decimal(str(bet_amount_float))
        except Exception:
            messagebox.showerror("Error", "Monto de apuesta inválido.")
            return

        # Verificamos si el usuario tiene saldo suficiente para la apuesta.
        if bet_amount > self.current_user['saldo']:
            messagebox.showerror("Error", "Saldo insuficiente")
            return

        # --- Lógica del Juego de la Máquina Tragamonedas ---
        symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"] # Símbolos posibles en los rodillos.
        results = [random.choice(symbols) for _ in range(3)] # Elegimos 3 símbolos aleatorios.

        win = Decimal('0.00') # Inicializamos las ganancias.
        message = ""          # Mensaje para el usuario.
        bet_result_status = 0 # 0 para pérdida, 1 para ganancia.

        # Evaluamos el resultado de la jugada.
        if results[0] == results[1] == results[2]: # Tres símbolos iguales (JACKPOT).
            win = bet_amount * Decimal('3')
            message = f"🎉 JACKPOT! Ganas ${win:.2f}"
            bet_result_status = 1
        elif results[0] == results[1] or results[1] == results[2]: # Dos símbolos iguales.
            win = bet_amount * Decimal('2')
            message = f"👍 Ganas ${win:.2f}"
            bet_result_status = 1
        else: # Ningún símbolo igual (pérdida).
            win = Decimal('0.00')
            message = "😢 Perdiste"
            bet_result_status = 0

        # --- Actualización del Saldo del Usuario ---
        # Calculamos el nuevo saldo restando la apuesta y sumando las ganancias.
        new_saldo = self.current_user['saldo'] + (win - bet_amount)
        # Actualizamos el saldo en la base de datos a través del modelo de usuario.
        self.user_model.update_user_balance(self.current_user['idcedula'], new_saldo)
        self.current_user['saldo'] = new_saldo # Actualizamos el saldo en los datos locales del usuario.
        self.view.update_saldo(new_saldo) # Le decimos a la Vista que actualice el saldo mostrado.

        # --- Registro de la Apuesta ---
        if self.bet_model: # Verificamos que el modelo de apuestas esté disponible.
            # Registramos la apuesta en la base de datos a través del modelo de apuestas.
            self.bet_model.create_bet(
                user_id=self.current_user['idcedula'],
                game_id=2, # Asumimos que la Máquina Tragamonedas tiene el ID de juego 2.
                amount=bet_amount,
                result=bet_result_status,
                winnings=win
            )
            if self.bet_controller: # Si el controlador de apuestas está disponible, refrescamos la lista de apuestas.
                self.bet_controller.load_user_bets()

        # --- Actualización de la Vista y Notificación ---
        self.view.display_results(results, message) # Le decimos a la Vista que muestre los resultados de la jugada.
        messagebox.showinfo("Resultado", message)   # Mostramos un mensaje emergente con el resultado.

        # --- Actualización del Dashboard ---
        # Si el controlador del dashboard está disponible, le pedimos que refresque los datos del usuario.
        # Esto asegura que el saldo en el dashboard se actualice después de cada jugada.
        if self.dashboard_controller:
            self.dashboard_controller.refresh_user_data()
