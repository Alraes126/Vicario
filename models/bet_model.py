# models/bet_model.py
# Este archivo define el Modelo para la gestión de datos de apuestas.
# Un modelo es responsable de interactuar con la base de datos para
# almacenar, recuperar y manipular la información de las apuestas.

# --- Definición de la Clase BetModel ---
# Esta clase sigue el principio de Responsabilidad Única (SRP)
# al encargarse exclusivamente de la persistencia y recuperación de datos de apuestas.
class BetModel:
    # El constructor (__init__) inicializa el modelo con un conector a la base de datos.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, db_connector):
        self.db = db_connector # Almacena la instancia del conector de la base de datos.

    # Método para obtener todas las apuestas registradas en la base de datos.
    def get_all_bets(self):
        query = "SELECT idapuesta, idcedula, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas"
        return self.db.execute_query(query) # Ejecuta la consulta y devuelve los resultados.

    # Método para obtener una apuesta específica por su ID.
    def get_bet_by_id(self, bet_id):
        query = "SELECT idapuesta, idcedula, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas WHERE idapuesta = %s"
        result = self.db.execute_query(query, (bet_id,)) # El '%s' es un placeholder para el parámetro.
        return result[0] if result else None # Devuelve la primera apuesta encontrada o None si no hay.

    # Método para obtener todas las apuestas realizadas por un usuario específico.
    # Permite filtrar las apuestas por un rango de fechas (opcional).
    def get_bets_by_user(self, user_id, start_date=None, end_date=None):
        query = "SELECT idapuesta, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas WHERE idcedula = %s"
        params = [user_id] # Lista para almacenar los parámetros de la consulta.

        # Si se proporciona una fecha de inicio, añadimos la condición al WHERE.
        if start_date:
            query += " AND fecha_apuesta >= %s"
            params.append(start_date)
        # Si se proporciona una fecha de fin, añadimos la condición al WHERE.
        if end_date:
            query += " AND fecha_apuesta <= %s"
            params.append(end_date)

        # Ejecutamos la consulta con todos los parámetros.
        return self.db.execute_query(query, tuple(params))

    # Método para crear una nueva apuesta en la base de datos.
    def create_bet(self, user_id, game_id, amount, result, winnings):
        query = """
        INSERT INTO apuestas (idcedula, idjuego, monto, resultado, ganancia)
        VALUES (%s, %s, %s, %s, %s)
        """
        # Los parámetros se pasan como una tupla para la consulta SQL.
        params = (user_id, game_id, amount, result, winnings)
        return self.db.execute_update(query, params) # Ejecuta la consulta de inserción.

    # TODO: Implement update_bet, delete_bet
    # Estos métodos se implementarían para actualizar o eliminar apuestas existentes.