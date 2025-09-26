# models/bet_model.py

class BetModel:
    def __init__(self, db_connector):
        self.db = db_connector

    def get_all_bets(self):
        query = "SELECT idapuesta, idcedula, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas"
        return self.db.execute_query(query)

    def get_bet_by_id(self, bet_id):
        query = "SELECT idapuesta, idcedula, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas WHERE idapuesta = %s"
        result = self.db.execute_query(query, (bet_id,))
        return result[0] if result else None

    def get_bets_by_user(self, user_id):
        query = "SELECT idapuesta, idjuego, monto, resultado, ganancia, fecha_apuesta FROM apuestas WHERE idcedula = %s"
        return self.db.execute_query(query, (user_id,))

    def create_bet(self, user_id, game_id, amount, result, winnings):
        query = """
        INSERT INTO apuestas (idcedula, idjuego, monto, resultado, ganancia)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (user_id, game_id, amount, result, winnings)
        return self.db.execute_update(query, params)

    # TODO: Implement update_bet, delete_bet
