import tkinter as tk
from tkinter import ttk, messagebox
import random
from models.user_model import UserModel
from models.game_model import GameModel
from controllers.slot_machine_controller import SlotMachineController

class SlotMachine:
    def __init__(self, root, db, user_placeholder, notebook):
        # Prepara la ventana de la máquina tragamonedas
        self.root = root # La ventana principal de la aplicación
        self.db = db # La conexión a la base de datos
        self.notebook = notebook # El sistema de pestañas de la aplicación
        
        # Creamos los modelos que necesitamos para interactuar con los datos
        self.user_model = UserModel(db) 
        self.game_model = GameModel(db)
        
        # Creamos el controlador que maneja la lógica del juego
        self.controller = SlotMachineController(self, self.game_model, self.user_model)

        # Limpiamos la ventana por si había algo antes
        for widget in self.root.winfo_children():
            widget.destroy()

        # Una bandera para saber si la animación de los rodillos está activa
        self.animation_running = False 
        self.create_widgets() # Creamos todos los botones y textos de la ventana
        
        # Si hay un usuario al iniciar, lo configuramos en el controlador
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)

    def create_widgets(self):
        # Esta función crea todos los elementos visuales de la máquina tragamonedas

        # Un recuadro principal para organizar todo
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Hacemos que la ventana se ajuste si cambiamos su tamaño
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Título de la máquina tragamonedas
        ttk.Label(frame, text="🎰 TRAGAMONEDAS", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        
        # Etiqueta para mostrar el saldo actual del jugador
        self.saldo_label = ttk.Label(frame, text=f"Saldo: $0.00")
        self.saldo_label.grid(row=1, column=0, pady=5)

        # Recuadro para los rodillos (donde giran los símbolos)
        self.slots_frame = ttk.Frame(frame)
        self.slots_frame.grid(row=2, column=0, pady=20)

        # Creamos las etiquetas que mostrarán los símbolos de los rodillos
        self.slots = []
        for i in range(3):
            label = ttk.Label(self.slots_frame, text="🍒", font=("Arial", 32), width=3)
            label.grid(row=0, column=i, padx=5)
            self.slots.append(label)

        # Recuadro para la apuesta
        bet_frame = ttk.Frame(frame)
        bet_frame.grid(row=3, column=0)
        # Etiqueta para el campo de apuesta
        ttk.Label(bet_frame, text="Apuesta:").grid(row=0, column=0, pady=5)
        # Campo para que el usuario elija cuánto apostar (con flechitas para subir/bajar)
        self.bet = ttk.Spinbox(bet_frame, from_=10, to=1000, increment=10, width=10)
        self.bet.grid(row=0, column=1, pady=5)
        self.bet.set(10) # Valor inicial de la apuesta

        # Botón para iniciar el juego
        ttk.Button(frame, text="JUGAR", command=self.play).grid(row=4, column=0, pady=10)
        # Botón para volver al panel principal
        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).grid(row=5, column=0, pady=5)

        # Etiqueta para mostrar el resultado de la jugada (ganaste, perdiste, etc.)
        self.result_label = ttk.Label(frame, text="", font=("Arial", 12))
        self.result_label.grid(row=6, column=0, pady=10)

    def update_saldo(self, new_saldo):
        # Actualiza el texto del saldo en la pantalla
        self.saldo_label.config(text=f"Saldo: ${new_saldo:.2f}")

    def display_results(self, results, message):
        # Muestra los símbolos finales en los rodillos y el mensaje de resultado
        for i, symbol in enumerate(results):
            self.slots[i].config(text=symbol)
        self.result_label.config(text=message)
        self.animation_running = False # La animación ha terminado

    def _start_animation(self, bet_amount):
        # Inicia la animación de los rodillos
        if self.animation_running:
            return # Si ya está girando, no hacemos nada

        self.animation_running = True # Marcamos que la animación está activa
        self.result_label.config(text="") # Borramos el resultado anterior
        
        # Símbolos que pueden aparecer en los rodillos durante la animación
        symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
        
        # Duración y pasos para la animación
        animation_duration_ms = 1500 # La animación durará 1.5 segundos
        steps_per_reel = 10 # Cada rodillo cambiará de símbolo 10 veces
        delay_per_step_ms = animation_duration_ms // steps_per_reel # El tiempo entre cada cambio de símbolo

        self.reels_stopped_count = 0 # Contador para saber cuántos rodillos se han detenido
        self.final_bet_amount = bet_amount # Guardamos la apuesta para cuando termine la animación

        for i in range(3):
            self._animate_reel(i, symbols, steps_per_reel, delay_per_step_ms)

    def _animate_reel(self, reel_index, symbols, remaining_steps, delay):
        # Anima un solo rodillo (cambia su símbolo varias veces)
        if remaining_steps > 0:
            # Cambia el símbolo del rodillo a uno al azar
            self.slots[reel_index].config(text=random.choice(symbols))
            # Programa el siguiente cambio de símbolo después de un pequeño retraso
            self.root.after(delay, self._animate_reel, reel_index, symbols, remaining_steps - 1, delay)
        else:
            # Cuando el rodillo termina de girar
            self.reels_stopped_count += 1 # Aumentamos el contador de rodillos detenidos
            if self.reels_stopped_count == 3: # Si todos los rodillos se han detenido
                # Llamamos al controlador para que calcule el resultado final y lo muestre
                self.controller.play_slot_machine(self.final_bet_amount)


    def play(self):
        # Esta función se ejecuta al presionar el botón "JUGAR"
        if self.animation_running:
            messagebox.showinfo("Juego en curso", "La máquina ya está girando. Espera a que termine.")
            return

        try:
            bet_amount = float(self.bet.get()) # Obtenemos la cantidad apostada
            # Iniciamos la animación. El controlador se llamará cuando la animación termine.
            self._start_animation(bet_amount)
        except ValueError:
            messagebox.showerror("Error", "Apuesta inválida. Introduce un número.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back_to_dashboard(self):
        # Esta función sirve para cambiar a la pestaña del panel de usuario (Dashboard)
        # TODO: Refrescar los datos del usuario en el dashboard antes de volver
        self.notebook.select(2)
