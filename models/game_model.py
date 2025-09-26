# models/game_model.py

class GameModel:
    def __init__(self, db_connector):
        self.db = db_connector

    def get_all_games(self):
        query = "SELECT idjuego, monto_minimo, nombre, estado, dificultad, probabilidad_ganar, categoria_probabilidad FROM juegos"
        return self.db.execute_query(query)

    def get_game_by_id(self, game_id):
        query = "SELECT idjuego, monto_minimo, nombre, estado, dificultad, probabilidad_ganar, categoria_probabilidad FROM juegos WHERE idjuego = %s"
        result = self.db.execute_query(query, (game_id,))
        return result[0] if result else None

    # TODO: Implement create_game, update_game, delete_game
