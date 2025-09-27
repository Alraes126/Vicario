# models/game_model.py
# Este archivo define el Modelo para la gestión de datos de juegos.
# Un modelo es responsable de interactuar con la base de datos para
# almacenar, recuperar y manipular la información de los diferentes juegos del casino.

# --- Definición de la Clase GameModel ---
# Esta clase sigue el principio de Responsabilidad Única (SRP)
# al encargarse exclusivamente de la persistencia y recuperación de datos de juegos.
class GameModel:
    # El constructor (__init__) inicializa el modelo con un conector a la base de datos.
    # Esto es un ejemplo de Inyección de Dependencias.
    def __init__(self, db_connector):
        self.db = db_connector # Almacena la instancia del conector de la base de datos.

    # Método para obtener todos los juegos disponibles en la base de datos.
    def get_all_games(self):
        query = "SELECT idjuego, monto_minimo, nombre, estado, dificultad, probabilidad_ganar, categoria_probabilidad FROM juegos"
        return self.db.execute_query(query) # Ejecuta la consulta y devuelve los resultados.

    # Método para obtener la información de un juego específico por su ID.
    def get_game_by_id(self, game_id):
        query = "SELECT idjuego, monto_minimo, nombre, estado, dificultad, probabilidad_ganar, categoria_probabilidad FROM juegos WHERE idjuego = %s"
        result = self.db.execute_query(query, (game_id,)) # El '%s' es un placeholder para el parámetro.
        return result[0] if result else None # Devuelve el primer juego encontrado o None si no hay.

    # TODO: Implement create_game, update_game, delete_game
    # Estos métodos se implementarían para añadir nuevos juegos, actualizar información
    # de juegos existentes o eliminar juegos de la base de datos.