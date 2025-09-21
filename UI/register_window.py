import tkinter as tk
from tkinter import ttk, messagebox

class RegisterWindow:
    def __init__(self, root, db):
        # Inicializa la ventana de registro
        # Guarda la ventana principal (root) y la conexión a la base de datos (db)
        self.root = root
        self.db = db
        # Llama a la función para crear todos los widgets de esta ventana
        self.create_widgets()

    def create_widgets(self):
        # Esta función crea todos los widgets de la ventana de registro

        # Crea un marco (frame) principal para organizar los widgets
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configura el sistema de grillas (grid) para que se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Aquí se crea la etiqueta para el título de la ventana
        ttk.Label(frame, text="📝 Registro Nuevo Usuario", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        self.entries = {}
        fields = ["Nombre", "Email", "Contraseña", "Edad", "Celular", "Apodo"]

        # Crea las etiquetas y campos de entrada para el formulario de rejistro
        for i, field in enumerate(fields):
            # Crea la etiqueta para el campo actual (ej "Nombre:")
            ttk.Label(frame, text=f"{field}:").grid(row=i + 1, column=0, pady=5, padx=5, sticky="w")
            # Crea el campo de entrada para el dato actual
            entry = ttk.Entry(frame, width=30)
            if field == "Contraseña":
                # Oculta la contraseña mientras se escribe
                entry.config(show="*")
            entry.grid(row=i + 1, column=1, pady=5, padx=5)
            self.entries[field.lower()] = entry

        # Aquí se crea el botón para registrar al nuevo usuario
        ttk.Button(frame, text="Registrar", command=self.register).grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    def register(self):
        # Esta función se ejecuta al presionar el botón "Registrar"
        
        # Obtiene los datos de los campos de entrada
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        # Valida que todos los campos estén completos
        if not all(data.values()):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        # Valida que la edad sea un número y que el usuario sea mayor de 18 años
        try:
            edad = int(data['edad'])
            if edad < 18:
                messagebox.showerror("Error", "Debes ser mayor de 18 años")
                return
        except ValueError:
            messagebox.showerror("Error", "Edad inválida")
            return

        # TODO: Implementar la lógica para guardar el usuario en la base de datos
        messagebox.showinfo("Éxito", "register complete")
