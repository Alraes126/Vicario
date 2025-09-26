# controllers/bet_controller.py

class BetController:
    def __init__(self, view, bet_model, user_model, game_model):
        self.view = view
        self.bet_model = bet_model
        self.user_model = user_model
        self.game_model = game_model
        self.current_user = None

    def set_current_user(self, user_data):
        self.current_user = user_data
        self.load_user_bets()

    def load_user_bets(self):
        if self.current_user:
            bets = self.bet_model.get_bets_by_user(self.current_user['idcedula'])
            # Enhance bet data with game name
            enhanced_bets = []
            for bet in bets:
                game = self.game_model.get_game_by_id(bet['idjuego'])
                bet['nombre_juego'] = game['nombre'] if game else 'Desconocido'
                enhanced_bets.append(bet)
            self.view.display_bets(enhanced_bets)
