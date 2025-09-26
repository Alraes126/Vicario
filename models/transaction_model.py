# models/transaction_model.py

class TransactionModel:
    def __init__(self, db_connector):
        self.db = db_connector

    def get_all_transactions(self):
        query = "SELECT idtransaccion, idcedula, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones"
        return self.db.execute_query(query)

    def get_transaction_by_id(self, transaction_id):
        query = "SELECT idtransaccion, idcedula, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones WHERE idtransaccion = %s"
        result = self.db.execute_query(query, (transaction_id,))
        return result[0] if result else None

    def get_transactions_by_user(self, user_id):
        query = "SELECT idtransaccion, tipo, metododepago, fecha_transaccion, monto_transaccion, estado FROM transacciones WHERE idcedula = %s"
        return self.db.execute_query(query, (user_id,))

    def create_transaction(self, transaction_data):
        query = """
        INSERT INTO transacciones (idcedula, tipo, metododepago, monto_transaccion, estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            transaction_data['idcedula'],
            transaction_data['tipo'],
            transaction_data['metododepago'],
            transaction_data['monto_transaccion'],
            transaction_data['estado']
        )
        return self.db.execute_update(query, params)

    # TODO: Implement create_transaction, update_transaction, delete_transaction
