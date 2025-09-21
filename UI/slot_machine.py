import tkinter as tk
from tkinter import ttk, messagebox
import random

class SlotMachine:
    def __init__(self, root, db, user, notebook):
        # Inicializa la ventana de la máquina tragamonedas
        # Guarda la ventana principal (root) la conexión a la base de datos (db)
        # el usuario (user) y el widget de pestañas (notebook)
        self.root = root
        self.db = db
        self.user = user
        self.notebook = notebook

        # Limpia la ventana principal de cualquier widget que existiera antes
        for widget in self.root.winfo_children():
            widget.destroy()

        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de la tragamonedas

        # Crea un marco (frame) principal para organizar los widgets
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configura el sistema de grillas (grid) para que se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Aquí se crea la etiqueta para el título de la ventana
        ttk.Label(frame, text="🎰 TRAGAMONEDAS", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        
        # Aquí se crea la etiqueta para mostrar el saldo del usuario
        self.saldo_label = ttk.Label(frame, text=f"Saldo: ${self.user['saldo']:.2f}")
        self.saldo_label.grid(row=1, column=0, pady=5)

        # Crea un marco para los rodillos de la tragamonedas
        self.slots_frame = ttk.Frame(frame)
        self.slots_frame.grid(row=2, column=0, pady=20)

        # Crea las etiquetas que representan los rodillos (slots)
        self.slots = []
        for i in range(3):
            label = ttk.Label(self.slots_frame, text="🍒", font=("Arial", 32), width=3)
            label.grid(row=0, column=i, padx=5)
            self.slots.append(label)

        # Crea un fram para el campo de la apuesta
        bet_frame = ttk.Frame(frame)
        bet_frame.grid(row=3, column=0)
        # Aquí se crea la etiqueta para el campo de apuesta
        ttk.Label(bet_frame, text="Apuesta:").grid(row=0, column=0, pady=5)
        # Aquí se crea el campo numérico (Spinbox el que tiene flechitas) para seleccionar la apuesta
        self.bet = ttk.Spinbox(bet_frame, from_=10, to=1000, increment=10, width=10)
        self.bet.grid(row=0, column=1, pady=5)
        self.bet.set(10)

        # Aquí se crea el botón para jugar
        ttk.Button(frame, text="JUGAR", command=self.play).grid(row=4, column=0, pady=10)
        # Aquí se crea el botón para volver al panel prinsipal
        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).grid(row=5, column=0, pady=5)

        # Aquí se crea la etiqueta para mostrar el resultado de la jugada
        self.result_label = ttk.Label(frame, text="", font=("Arial", 12))
        self.result_label.grid(row=6, column=0, pady=10)

    def play(self):
        # Esta función se ejecuta al presionar el botón "JUGAR"
        try:
            bet_amount = float(self.bet.get())
            # Verifica si el usuario tiene saldo suficiente para la apuesta
            if bet_amount > self.user['saldo']:
                messagebox.showerror("Error", "Saldo insuficiente")
                return

            # Símbolos posibles en los rodillos
            symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
            # Elige 3 símbolos al azar para simular el giro
            results = [random.choice(symbols) for _ in range(3)]

            # Actualiza el texto de las etiquetas de los rodillos con los nuevos símbolos
            for i, symbol in enumerate(results):
                self.slots[i].config(text=symbol)

            # Verifica el resultado para ver si hay premio
            if results[0] == results[1] == results[2]:
                win = bet_amount * 3
                message = f"🎉 JACKPOT! Ganas ${win:.2f}"
            elif results[0] == results[1] or results[1] == results[2]:
                win = bet_amount * 2
                message = f"👍 Ganas ${win:.2f}"
            else:
                win = 0
                message = "😢 Perdiste"

            # Muestra el mensaje de resultado en la etiqueta correspondiente
            self.result_label.config(text=message)

            # Actualiza el saldo del usuario en la interfaz
            self.user['saldo'] += (win - bet_amount)
            self.saldo_label.config(text=f"Saldo: ${self.user['saldo']:.2f}")
            # Muestra una ventana emergente con el resultado
            messagebox.showinfo("Resultado", message)


        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back_to_dashboard(self):
        # Esta función sirve para cambiar a la pestaña del panel de usuario (Dashboard)
        self.notebook.select(2) # Asume que el Dashboard es la tercera pestaña (índice 2)