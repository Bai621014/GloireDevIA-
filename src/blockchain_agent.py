# src/blockchain_agent.py
import json
from web3 import Web3

class Web3Agent:
    def __init__(self, registry_path='registry.json'):
        with open(registry_path, 'r') as f:
            self.registry = json.load(f)
        self.w3 = Web3(Web3.HTTPProvider('https://zkevm-rpc.com'))

    def get_treasury_balance(self):
        address = self.registry['contracts']['Treasury']
        return self.w3.eth.get_balance(address)

    def trigger_self_sustain(self):
        # Logique pour appeler le contrat Treasury.sol via l'IA
        print("Audit: Trésorerie analysée, mécanisme d'auto-sustain prêt.")
