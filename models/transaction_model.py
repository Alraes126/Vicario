# models/transaction_model.py
# Este archivo define el Modelo para la gestión de datos de transacciones.
# Un modelo es responsable de interactuar con la base de datos para
# almacenar, recuperar y manipular la información de las transacciones (ej. depósitos).

# --- Definición de la Clase TransactionModel ---
# Esta clase sigue el principio de Responsabilidad Única (SRP)
# al encargarse exclusivamente de la persistencia y recuperación de datos de transacciones.
class TransactionModel:
    # El constructor (__init__) inicializa el modelo con un conector a la base de datos.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, db_connector):
        self.db = db_connector # Almacena la instancia del conector de la base de datos.

    # Método para obtener todas las transacciones registradas en la base de datos.
    def get_all_transactions(self):
        query = "SELECT idtransaccion, idcedula, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones"
        return self.db.execute_query(query) # Ejecuta la consulta y devuelve los resultados.

    # Método para obtener una transacción específica por su ID.
    def get_transaction_by_id(self, transaction_id):
        query = "SELECT idtransaccion, idcedula, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones WHERE idtransaccion = %s"
        result = self.db.execute_query(query, (transaction_id,)) # El '%s' es un placeholder para el parámetro.
        return result[0] if result else None # Devuelve la primera transacción encontrada o None si no hay.

    # Método para obtener todas las transacciones realizadas por un usuario específico.
    # Permite filtrar las transacciones por un rango de fechas (opcional).
    def get_transactions_by_user(self, user_id, start_date=None, end_date=None):
        query = "SELECT idtransaccion, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones WHERE idcedula = %s"
        params = [user_id] # Lista para almacenar los parámetros de la consulta.

        # Si se proporciona una fecha de inicio, añadimos la condición al WHERE.
        if start_date:
            query += " AND fecha_transaccion >= %s"
            params.append(start_date)
        # Si se proporciona una fecha de fin, añadimos la condición al WHERE.
        if end_date:
            query += " AND fecha_transaccion <= %s"
            params.append(end_date)

        # Ejecutamos la consulta con todos los parámetros.
        return self.db.execute_query(query, tuple(params))

    # Método para crear una nueva transacción en la base de datos.
    def create_transaction(self, transaction_data):
        query = """
        INSERT INTO transacciones (idcedula, tipo, metododepago, monto_transaccion, estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        # Los parámetros se pasan como una tupla para la consulta SQL.
        params = (
            transaction_data['idcedula'],
            transaction_data['tipo'],
            transaction_data['metododepago'],
            transaction_data['monto_transaccion'],
            transaction_data['estado']
        )
        return self.db.execute_update(query, params) # Ejecuta la consulta de inserción.

    # TODO: Implement create_transaction, update_transaction, delete_transaction
    # Estos métodos se implementarían para actualizar o eliminar transacciones existentes.