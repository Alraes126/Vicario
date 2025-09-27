import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk, filedialog # Importamos ttk para widgets con estilos modernos y filedialog para diálogos de archivo.
import datetime # Importamos datetime para trabajar con fechas.
from tkcalendar import DateEntry # Importamos DateEntry de tkcalendar para un selector de fechas amigable.

# Importamos los Modelos y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from models.game_model import GameModel
from models.bet_model import BetModel
from controllers.bet_controller import BetController

# --- Definición de la Clase BetsWindow ---
# Esta clase representa la Vista (GUI) para mostrar el historial de apuestas del usuario.
# Es responsable de cómo se ve y cómo el usuario interactúa con la información de apuestas.
class BetsWindow:
    # El constructor (__init__) inicializa la ventana de apuestas.
    # Recibe la ventana raíz, el conector de la base de datos, un placeholder de usuario y el widget de pestañas.
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        self.notebook = notebook     # El widget de pestañas (ttk.Notebook) para cambiar entre vistas.
        
        # Inicializamos los Modelos que este controlador podría necesitar indirectamente.
        # Aunque la vista no interactúa directamente con ellos, el controlador sí.
        self.user_model = UserModel(db)
        self.game_model = GameModel(db)
        self.bet_model = BetModel(db)
        
        # Creamos una instancia del Controlador de Apuestas, pasándole esta vista y los modelos.
        # Esto establece la conexión entre la Vista y su Controlador.
        self.controller = BetController(self, self.bet_model, self.user_model, self.game_model)

        # Limpiamos la ventana principal de cualquier widget que pudiera haber antes.
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.
        
        # Si se pasa un usuario al inicializar la ventana, lo establecemos en el controlador.
        if user_placeholder:
            self.controller.set_current_user(user_placeholder)
        self.load_bets() # Cargamos las apuestas iniciales del usuario.

    # Método para crear y organizar todos los widgets (botones, etiquetas, tablas) de la ventana.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal para organizar los elementos.
        frame.pack(fill=tk.BOTH, expand=True) # Empaquetamos el marco para que ocupe todo el espacio.

        # Etiqueta de título para la ventana de apuestas.
        ttk.Label(frame, text="🎯 MIS APUESTAS", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Sección de Filtro por Fecha ---
        # Creamos un marco con etiqueta para agrupar los controles de filtro por fecha.
        filter_frame = ttk.LabelFrame(frame, text="Filtrar por Fecha", padding=10)
        filter_frame.pack(pady=10, padx=10, fill="x")

        # Etiqueta y selector de fecha "Desde".
        ttk.Label(filter_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Etiqueta y selector de fecha "Hasta".
        ttk.Label(filter_frame, text="Hasta:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.end_date_entry = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Botón para aplicar el filtro de fechas.
        ttk.Button(filter_frame, text="Aplicar Filtro", command=self.apply_filter).grid(row=0, column=4, padx=10, pady=5)
        # --- Fin Sección de Filtro por Fecha ---

        # --- Tabla (Treeview) para Mostrar Apuestas ---
        # Definimos las columnas que tendrá nuestra tabla de apuestas.
        columns = ("ID", "Juego", "Monto", "Resultado", "Ganancia", "Fecha")
        # Creamos el widget Treeview, que es una tabla avanzada de Tkinter.
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        # Configuramos los encabezados de cada columna.
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100) # Definimos un ancho para cada columna.

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True) # Empaquetamos la tabla.

        # --- Botones de Exportación ---
        # Creamos un marco para agrupar los botones de exportación.
        export_frame = ttk.Frame(frame)
        export_frame.pack(pady=10, fill="x")

        # Botón para exportar a PDF.
        ttk.Button(export_frame, text="Exportar a PDF", command=self.export_to_pdf).pack(side=tk.LEFT, padx=5, expand=True)
        # Botón para exportar a Excel.
        ttk.Button(export_frame, text="Exportar a Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=5, expand=True)
        # --- Fin Botones de Exportación ---

        # Botón para volver al Dashboard.
        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).pack(pady=10)

    # Método para mostrar las apuestas en la tabla (Treeview).
    def display_bets(self, bets):
        # Limpiamos cualquier entrada existente en la tabla antes de añadir nuevas.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertamos cada apuesta en la tabla.
        for bet in bets:
            self.tree.insert("", "end", values=(
                bet['idapuesta'],
                bet['nombre_juego'], # Usamos el nombre del juego enriquecido por el controlador.
                f"${bet['monto']:.2f}", # Formateamos el monto como moneda.
                bet['resultado'],
                f"${bet['ganancia']:.2f}", # Formateamos la ganancia como moneda.
                bet['fecha_apuesta']
            ))

    # Método para cargar las apuestas del usuario.
    # Simplemente delega la tarea al controlador.
    def load_bets(self):
        self.controller.load_user_bets()

    # Método que se ejecuta cuando el usuario hace clic en "Aplicar Filtro".
    def apply_filter(self):
        # Obtenemos las fechas seleccionadas de los selectores de fecha.
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        # Convertimos las fechas a formato de cadena 'YYYY-MM-DD' para pasarlas al modelo.
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

        # Le pedimos al controlador que cargue las apuestas con los filtros aplicados.
        self.controller.load_user_bets(start_date_str, end_date_str)

    # Método que se ejecuta cuando el usuario hace clic en "Exportar a PDF".
    def export_to_pdf(self):
        # Obtenemos las apuestas actualmente mostradas en la tabla.
        # Asumimos que la tabla refleja con precisión los datos filtrados.
        bets_to_export = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            # Reconstruimos un diccionario de apuesta para el exportador.
            bets_to_export.append({
                'idapuesta': values[0],
                'nombre_juego': values[1],
                'monto': float(values[2].replace('$', '')), # Convertimos el monto a float, quitando el '$’.
                'resultado': values[3],
                'ganancia': float(values[4].replace('$', '')), # Convertimos la ganancia a float, quitando el '$’.
                'fecha_apuesta': values[5]
            })
        
        # Abrimos un diálogo para que el usuario elija dónde guardar el archivo PDF.
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path: # Si el usuario seleccionó una ruta...
            self.controller.export_bets_to_pdf(bets_to_export, file_path) # Le pedimos al controlador que exporte.

    # Método que se ejecuta cuando el usuario hace clic en "Exportar a Excel".
    def export_to_excel(self):
        # Obtenemos las apuestas actualmente mostradas en la tabla.
        bets_to_export = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            bets_to_export.append({
                'idapuesta': values[0],
                'nombre_juego': values[1],
                'monto': float(values[2].replace('$', '')), # Convertimos el monto a float, quitando el '$’.
                'resultado': values[3],
                'ganancia': float(values[4].replace('$', '')), # Convertimos la ganancia a float, quitando el '$’.
                'fecha_apuesta': values[5]
            })

        # Abrimos un diálogo para que el usuario elija dónde guardar el archivo Excel.
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path: # Si el usuario seleccionó una ruta...
            self.controller.export_bets_to_excel(bets_to_export, file_path) # Le pedimos al controlador que exporte.

    # Método para volver a la pestaña del Dashboard.
    def back_to_dashboard(self):
        # Seleccionamos la pestaña del Dashboard en el notebook.
        # Asumimos que el Dashboard es la tercera pestaña (índice 2).
        self.notebook.select(2)
