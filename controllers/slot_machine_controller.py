# controllers/slot_machine_controller.py
import random
from tkinter import messagebox
from decimal import Decimal # Added import

class SlotMachineController:
    def __init__(self, view, game_model, user_model):
        self.view = view
        self.game_model = game_model
        self.user_model = user_model
        self.current_user = None # To store the logged-in user's data
        self.bet_model = None # New: Will be set by DashboardController
        self.bet_controller = None # New: Will be set by DashboardController

    def set_current_user(self, user_data):
        self.current_user = user_data
        self.view.update_saldo(user_data['saldo'])

    def play_slot_machine(self, bet_amount_float): # Renamed parameter for clarity
        if not self.current_user:
            messagebox.showerror("Error", "No hay usuario logueado.")
            return

        try:
            bet_amount = Decimal(str(bet_amount_float)) # Convert float to Decimal
        except Exception:
            messagebox.showerror("Error", "Monto de apuesta inválido.")
            return

        if bet_amount > self.current_user['saldo']:
            messagebox.showerror("Error", "Saldo insuficiente")
            return

        symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
        results = [random.choice(symbols) for _ in range(3)]

        win = Decimal('0.00') # Initialize win as Decimal
        message = ""
        bet_result_status = 0 # 0 for loss, 1 for win

        if results[0] == results[1] == results[2]:
            win = bet_amount * Decimal('3')
            message = f"🎉 JACKPOT! Ganas ${win:.2f}"
            bet_result_status = 1
        elif results[0] == results[1] or results[1] == results[2]:
            win = bet_amount * Decimal('2')
            message = f"👍 Ganas ${win:.2f}"
            bet_result_status = 1
        else:
            win = Decimal('0.00')
            message = "😢 Perdiste"
            bet_result_status = 0

        # Debug prints for types
        print(f"DEBUG: SlotMachineController - Type of self.current_user['saldo']: {type(self.current_user['saldo'])}, Value: {self.current_user['saldo']}")
        print(f"DEBUG: SlotMachineController - Type of bet_amount: {type(bet_amount)}, Value: {bet_amount}")
        print(f"DEBUG: SlotMachineController - Type of win: {type(win)}, Value: {win}")

        # Update user balance
        new_saldo = self.current_user['saldo'] + (win - bet_amount)
        self.user_model.update_user_balance(self.current_user['idcedula'], new_saldo)
        self.current_user['saldo'] = new_saldo # Update local user data
        self.view.update_saldo(new_saldo) # Update view

        # Record the bet
        if self.bet_model: # Ensure bet_model is available
            self.bet_model.create_bet(
                user_id=self.current_user['idcedula'],
                game_id=2, # Assuming Slot Machine is game_id 2 (from database.db)
                amount=bet_amount,
                result=bet_result_status,
                winnings=win
            )
            if self.bet_controller: # Refresh bets list if controller is available
                self.bet_controller.load_user_bets()

        self.view.display_results(results, message)
        messagebox.showinfo("Resultado", message)