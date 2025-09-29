import tkinter as tk # Importamos la biblioteca principal para crear interfaces gráficas.
from tkinter import ttk, messagebox, filedialog # Importamos ttk para widgets con estilos modernos, messagebox para mensajes emergentes, y filedialog para abrir diálogos de selección de archivo.
import datetime # Importamos datetime para trabajar con fechas.
from tkcalendar import DateEntry # Importamos DateEntry de tkcalendar para un selector de fechas amigable.

# Importamos los Modelos y el Controlador necesarios para esta vista.
# Esto es parte del patrón Modelo-Vista-Controlador (MVC).
from models.user_model import UserModel
from models.transaction_model import TransactionModel
from controllers.transaction_controller import TransactionController

# --- Definición de la Clase TransactionsWindow ---
# Esta clase representa la Vista (GUI) para mostrar el historial de transacciones del usuario.
# Es responsable de cómo se ve y cómo el usuario interactúa con la información de transacciones.
class TransactionsWindow:
    # El constructor (__init__) inicializa la ventana de transacciones.
    # Recibe la ventana raíz, el conector de la base de datos, un placeholder de usuario y el widget de pestañas.
    def __init__(self, root, db, user_placeholder, notebook):
        self.root = root             # La ventana principal de la aplicación.
        self.db = db                 # El conector a la base de datos.
        self.notebook = notebook     # El widget de pestañas (ttk.Notebook) para cambiar entre vistas.
        
        # Inicializamos los Modelos que este controlador podría necesitar indirectamente.
        self.user_model = UserModel(db)
        self.transaction_model = TransactionModel(db)
        
        # Creamos una instancia del Controlador de Transacciones, pasándole esta vista y los modelos.
        # Esto establece la conexión entre la Vista y su Controlador.
        self.controller = TransactionController(self, self.transaction_model, self.user_model)

        # Limpiamos la ventana principal de cualquier widget que pudiera haber antes.
        for widget in self.root.winfo_children():
            widget.destroy()

        self.deposit_amount_entry = None # Campo de entrada para el monto del depósito.
        self.payment_method_var = tk.StringVar() # Variable para almacenar el método de pago seleccionado.
        
        self.create_widgets() # Llamamos a un método para construir todos los elementos de la GUI.
        


    # Método para crear y organizar todos los widgets (campos de entrada, botones, tablas) de la ventana.
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20) # Creamos un marco principal para organizar los elementos.
        frame.pack(fill=tk.BOTH, expand=True) # Empaquetamos el marco para que ocupe todo el espacio.

        # Etiqueta de título para la ventana de transacciones.
        ttk.Label(frame, text="💳 MIS TRANSACCIONES", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Sección de Depósito ---
        # Creamos un marco con etiqueta para agrupar los controles de depósito.
        deposit_frame = ttk.LabelFrame(frame, text="Realizar Depósito", padding=10)
        deposit_frame.pack(pady=10, padx=10, fill="x")

        # Registramos una función de validación para asegurar que el monto sea numérico.
        validate_cmd = self.root.register(self.validate_numeric_input)

        # Etiqueta y campo de entrada para el monto del depósito.
        ttk.Label(deposit_frame, text="Monto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.deposit_amount_entry = ttk.Entry(deposit_frame, width=20, validate="key", validatecommand=(validate_cmd, '%P'))
        self.deposit_amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Etiqueta y menú desplegable para el metodode pago
        ttk.Label(deposit_frame, text="Método de Pago:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        payment_methods = ['PSE', 'transferencia de ciertos bancos', 'bancolombia']
        self.payment_method_optionmenu = ttk.OptionMenu(deposit_frame, self.payment_method_var, payment_methods[0], *payment_methods)
        self.payment_method_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Botón para iniciar el depósito.
        ttk.Button(deposit_frame, text="Depositar", command=self.make_deposit_request).grid(row=2, column=0, columnspan=2, pady=10)
        # --- Fin Sección de Depósito ---

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
        # Botones de exportación dentro del marco de filtro.
        ttk.Button(filter_frame, text="Exportar PDF", command=self.export_to_pdf).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(filter_frame, text="Exportar Excel", command=self.export_to_excel).grid(row=0, column=6, padx=5, pady=5)
        # --- Fin Sección de Filtro por Fecha ---

        # --- Tabla (Treeview) para Mostrar Transacciones ---
        # Definimos las columnas que tendrá nuestra tabla de transacciones.
        columns = ("ID", "Tipo", "Monto", "Fecha", "Estado")
        # Creamos el widget Treeview, que es una tabla avanzada de Tkinter.
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        # Configuramos los encabezados de cada columna.
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100) # Definimos un ancho para cada columna.

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True) # Empaquetamos la tabla.

        # Botón para volver al Dashboard.
        ttk.Button(frame, text="Volver", command=self.back_to_dashboard).pack(pady=10)

    # Metodo de validación para asegurar que la entrada sea numerica
    # Se usa con 'validatecommand' en los campos de entrada.
    def validate_numeric_input(self, value_if_allowed):
        if value_if_allowed == "": # Permitimos que el campo esté vacío.
            return True
        try:
            float(value_if_allowed) # Intentamos convertir el valor a flotante.
            return True             # Si es exitoso, el valor es numérico.
        except ValueError:
            return False            # Si falla, no es numérico.

    # Método para mostrar las transacciones en la tabla (Treeview).
    def display_transactions(self, transactions):
        # Limpiamos cualquier entrada existente en la tabla antes de añadir nuevas.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertamos cada transacción en la tabla.
        for trans in transactions:
            self.tree.insert("", "end", values=(
                trans['idtransaccion'],
                trans['tipo'],
                f"${trans['monto_transaccion']:.2f}", # Formateamos el monto como moneda.
                trans['fecha_transaccion'],
                trans['estado']
            ))

    # Método para cargar las transacciones del usuario.
    # Simplemente delega la tarea al controlador.
    def load_transactions(self):
        self.controller.load_user_transactions()

    # Método que se ejecuta cuando el usuario hace clic en "Realizar Depósito".
    def make_deposit_request(self):
        amount_str = self.deposit_amount_entry.get() # Obtenemos el monto del campo de entrada.
        if not amount_str: # Validamos que el monto no esté vacío.
            messagebox.showerror("Error", "El monto no puede estar vacío.")
            return

        payment_method = self.payment_method_var.get() # Obtenemos el método de pago seleccionado.
        
        # --- Diálogo de Confirmación ---
        # Mostramos un mensaje de confirmación antes de realizar una operación crítica.
        confirm = messagebox.askyesno("Confirmar Depósito", f"¿Estás seguro de que deseas depositar ${amount_str} usando {payment_method}?")
        if confirm: # Si el usuario confirma...
            self.controller.request_deposit(amount_str, payment_method) # Le pedimos al controlador que procese el depósito.

    # Método que se ejecuta cuando el usuario hace clic en "Aplicar Filtro".
    def apply_filter(self):
        # Obtenemos las fechas seleccionadas de los selectores de fecha.
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        # Convertimos las fechas a formato de cadena 'YYYY-MM-DD' para pasarlas al modelo.
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

        # Le pedimos al controlador que cargue las transacciones con los filtros aplicados.
        self.controller.load_user_transactions(start_date_str, end_date_str)

    # Método que se ejecuta cuando el usuario hace clic en "Exportar a PDF".
    def export_to_pdf(self):
        # Obtenemos las transacciones actualmente mostradas en la tabla.
        # Asumimos que la tabla refleja con precisión los datos filtrados.
        transactions_to_export = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            # Reconstruimos un diccionario de transacción para el exportador.
            transactions_to_export.append({
                'idtransaccion': values[0],
                'tipo': values[1],
                'metododepago': "N/A", # El método de pago no está directamente en la tabla, lo marcamos como N/A.
                'monto_transaccion': float(values[2].replace('$', '')), # Convertimos el monto a float, quitando el '$’.
                'fecha_transaccion': values[3],
                'estado': values[4]
            })
        
        # Abrimos un diálogo para que el usuario elija dónde guardar el archivo PDF.
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path: # Si el usuario seleccionó una ruta...
            self.controller.export_transactions_to_pdf(transactions_to_export, file_path) # Le pedimos al controlador que exporte.

    # Método que se ejecuta cuando el usuario hace clic en "Exportar a Excel".
    def export_to_excel(self):
        # Obtenemos las transacciones actualmente mostradas en la tabla.
        transactions_to_export = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            transactions_to_export.append({
                'idtransaccion': values[0],
                'tipo': values[1],
                'metododepago': "N/A", # El método de pago no está directamente en la tabla, lo marcamos como N/A.
                'monto_transaccion': float(values[2].replace('$', '')), # Convertimos el monto a float, quitando el '$’.
                'fecha_transaccion': values[3],
                'estado': values[4]
            })

        # Abrimos un diálogo para que el usuario elija dónde guardar el archivo Excel.
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path: # Si el usuario seleccionó una ruta...
            self.controller.export_transactions_to_excel(transactions_to_export, file_path) # Le pedimos al controlador que exporte.

    # Método para volver a la pestaña del Dashboard.
    def back_to_dashboard(self):
        # Seleccionamos la pestaña del Dashboard en el notebook.
        # Asumimos que el Dashboard es la tercera pestaña (índice 2).
        self.notebook.select(2)