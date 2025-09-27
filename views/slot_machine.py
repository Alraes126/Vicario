import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk, messagebox # Importamos ttk para widgets con estilos modernos y messagebox para mensajes emergentes.
import random # Importamos random para generar resultados aleatorios en el juego.

# Importamos los Modelos y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from models.game_model import GameModel
from controllers.slot_machine_controller import SlotMachineController

# --- Definición de la Clase SlotMachine ---
# Esta clase representa la Vista (GUI) para la máquina tragamonedas.
# Es responsable de cómo se ve el juego y cómo el usuario interactúa con él.
class SlotMachine:
    # El constructor (__init__) inicializa la ventana de la máquina tragamonedas.
    # Recibe la ventana raíz, el conector de la base de datos, un placeholder de usuario y el widget de pestañas.
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        self.notebook = notebook     # El widget de pestañas (ttk.Notebook) para cambiar entre vistas.
        
        # Inicializamos los Modelos que este controlador podría necesitar indirectamente.
        self.user_model = UserModel(db)
        self.game_model = GameModel(db)
        
        # Creamos una instancia del Controlador de la Máquina Tragamonedas, pasándole esta vista y los modelos.
        # Esto establece la conexión entre la Vista y su Controlador.
        self.controller = SlotMachineController(self, self.game_model, self.user_model)

        # Limpiamos la ventana por si había algo antes.
        for widget in self.root.winfo_children():
            widget.destroy()

        self.animation_running = False # Una bandera para saber si la animación de los rodillos está activa.
        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.
        
        # Si hay un usuario al iniciar, lo configuramos en el controlador.
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)

    # Método para crear y organizar todos los widgets (rodillos, botones, etiquetas) de la ventana.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal para organizar los elementos.
        frame.grid(row=0, column=0, sticky="nsew") # Usamos grid para posicionar el marco.

        # Configuramos el sistema de grillas para que el marco se expanda correctamente.
        self.root.grid_row_configure(0, weight=1)
        self.root.grid_column_configure(0, weight=1)
        frame.grid_column_configure(0, weight=1)

        # Etiqueta de título para la máquina tragamonedas.
        ttk.Label(frame, text="🎰 TRAGAMONEDAS", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        
        # Etiqueta para mostrar el saldo actual del jugador.
        self.saldo_label = ttk.Label(frame, text=f"Saldo: $0.00")
        self.saldo_label.grid(row=1, column=0, pady=5)

        # Marco para los rodillos (donde giran los símbolos).
        self.slots_frame = ttk.Frame(frame)
        self.slots_frame.grid(row=2, column=0, pady=20)

        # Creamos las etiquetas que mostrarán los símbolos de los rodillos.
        self.slots = []
        for i in range(3):
            label = ttk.Label(self.slots_frame, text="🍒", font=("Arial", 32), width=3)
            label.grid(row=0, column=i, padx=5)
            self.slots.append(label)

        # Marco para la sección de apuesta.
        bet_frame = ttk.Frame(frame)
        bet_frame.grid(row=3, column=0)
        # Etiqueta para el campo de apuesta.
        ttk.Label(bet_frame, text="Apuesta:").grid(row=0, column=0, pady=5)
        # Campo para que el usuario elija cuánto apostar (Spinbox permite subir/bajar valores).
        self.bet = ttk.Spinbox(bet_frame, from_=10, to=1000, increment=10, width=10)
        self.bet.grid(row=0, column=1, pady=5)
        self.bet.set(10) # Valor inicial de la apuesta.

        # Botón para iniciar el juego. Al hacer clic, llama al método 'play'.
        ttk.Button(frame, text="JUGAR", command=self.play).grid(row=4, column=0, pady=10)
        # Botón para volver al panel principal.
        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).grid(row=5, column=0, pady=5)

        # Etiqueta para mostrar el resultado de la jugada (ganaste, perdiste, etc.).
        self.result_label = ttk.Label(frame, text="", font=("Arial", 12))
        self.result_label.grid(row=6, column=0, pady=10)

    # Método para actualizar el texto del saldo en la pantalla.
    def update_saldo(self, new_saldo):
        self.saldo_label.config(text=f"Saldo: ${new_saldo:.2f}")

    # Método para mostrar los símbolos finales en los rodillos y el mensaje de resultado.
    def display_results(self, results, message):
        for i, symbol in enumerate(results):
            self.slots[i].config(text=symbol)
        self.result_label.config(text=message)
        self.animation_running = False # La animación ha terminado.

    # Método privado para iniciar la animación de los rodillos.
    def _start_animation(self, bet_amount):
        if self.animation_running: # Si ya está girando, no hacemos nada.
            return

        self.animation_running = True # Marcamos que la animación está activa.
        self.result_label.config(text="") # Borramos el resultado anterior.
        
        # Símbolos que pueden aparecer en los rodillos durante la animación.
        symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
        
        # Duración y pasos para la animación.
        animation_duration_ms = 1500 # La animación durará 1.5 segundos.
        steps_per_reel = 10          # Cada rodillo cambiará de símbolo 10 veces.
        delay_per_step_ms = animation_duration_ms // steps_per_reel # El tiempo entre cada cambio de símbolo.

        self.reels_stopped_count = 0 # Contador para saber cuántos rodillos se han detenido.
        self.final_bet_amount = bet_amount # Guardamos la apuesta para cuando termine la animación.

        for i in range(3): # Iniciamos la animación para cada uno de los tres rodillos.
            self._animate_reel(i, symbols, steps_per_reel, delay_per_step_ms)

    # Método privado para animar un solo rodillo (cambia su símbolo varias veces).
    def _animate_reel(self, reel_index, symbols, remaining_steps, delay):
        if remaining_steps > 0:
            # Cambia el símbolo del rodillo a uno al azar.
            self.slots[reel_index].config(text=random.choice(symbols))
            # Programa el siguiente cambio de símbolo después de un pequeño retraso.
            self.root.after(delay, self._animate_reel, reel_index, symbols, remaining_steps - 1, delay)
        else:
            # Cuando el rodillo termina de girar.
            self.reels_stopped_count += 1 # Aumentamos el contador de rodillos detenidos.
            if self.reels_stopped_count == 3: # Si todos los rodillos se han detenido...
                # Llamamos al controlador para que calcule el resultado final y lo muestre.
                self.controller.play_slot_machine(self.final_bet_amount)

    # Método que se ejecuta al presionar el botón "JUGAR".
    def play(self):
        if self.animation_running: # Si la animación ya está en curso, mostramos un mensaje.
            messagebox.showinfo("Juego en curso", "La máquina ya está girando. Espera a que termine.")
            return

        try:
            bet_amount = float(self.bet.get()) # Obtenemos la cantidad apostada del Spinbox.
            # Iniciamos la animación. El controlador se llamará cuando la animación termine.
            self._start_animation(bet_amount)
        except ValueError: # Capturamos errores si la apuesta no es un número válido.
            messagebox.showerror("Error", "Apuesta inválida. Introduce un número.")
        except Exception as e: # Capturamos cualquier otro error.
            messagebox.showerror("Error", str(e))

    # Método para volver a la pestaña del Dashboard.
    def back_to_dashboard(self):
        # Seleccionamos la pestaña del Dashboard en el notebook.
        # Asumimos que el Dashboard es la tercera pestaña (índice 2).
        self.notebook.select(2)