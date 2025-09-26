# controllers/dashboard_controller.py

class DashboardController:
    def __init__(self, view, user_model):
        self.view = view
        self.user_model = user_model
        self.current_user = None
        self.slot_machine_controller = None
        self.bet_controller = None
        self.transaction_controller = None

    def set_current_user(self, user_data):
        self.current_user = user_data
        self.view.update_dashboard(user_data)
        
        # Propagate updated user data to other controllers
        if self.slot_machine_controller:
            self.slot_machine_controller.set_current_user(user_data)
            # Also pass bet_model and bet_controller to slot_machine_controller
            self.slot_machine_controller.bet_model = self.bet_controller.bet_model # Assuming bet_controller has bet_model
            self.slot_machine_controller.bet_controller = self.bet_controller
        if self.bet_controller:
            self.bet_controller.set_current_user(user_data)
        if self.transaction_controller:
            self.transaction_controller.set_current_user(user_data)

    def refresh_user_data(self):
        if self.current_user:
            updated_user = self.user_model.get_user_by_id(self.current_user['idcedula'])
            if updated_user:
                self.set_current_user(updated_user)
            else:
                print("Error: Could not refresh user data.")
