import os
from web3 import Web3

class GloireWeb3Manager:
    def __init__(self, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.address = "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d" # Votre adresse de trésorerie

    def estimate_maintenance_cost(self):
        # Estimation basique du coût de transaction en Wei
        gas_price = self.w3.eth.gas_price
        gas_limit = 21000
        return gas_price * gas_limit

    def get_treasury_status(self):
        if not self.w3.is_connected():
            return {"status": "ERROR", "message": "Nœud déconnecté"}
        
        balance = self.w3.eth.get_balance(self.address)
        balance_eth = self.w3.from_wei(balance, 'ether')
        
        # Logique de conformité : faut au moins 0.0001 ETH pour opérer
        if balance_eth >= 0.0001:
            return {"status": "COMPLIANT", "balance_eth": balance_eth}
        else:
            return {"status": "NON-COMPLIANT", "message": "Solde insuffisant"}
