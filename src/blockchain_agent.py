    def estimate_maintenance_cost(self):
        """Calcule le coût théorique de la transaction avec marge de sécurité"""
        try:
            gas_price = self.w3.eth.gas_price
            # Multiplier par 1.1 (10% de marge) pour éviter le 'Out of Gas'
            return int(gas_price * 200000 * 1.1)
        except Exception as e:
            return 0 # Retourne 0 en cas de défaillance RPC

    def get_treasury_status(self):
        """Sécurisé pour gérer les erreurs réseau"""
        try:
            treasury_addr = self.registry['contracts']['Treasury']
            balance = self.w3.eth.get_balance(treasury_addr)
            return {"address": treasury_addr, "balance_wei": balance, "status": "online"}
        except Exception as e:
            return {"address": None, "balance_wei": 0, "status": "error", "message": str(e)}
