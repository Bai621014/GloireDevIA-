import os
from web3 import Web3

# Récupération de l'URL depuis les secrets GitHub
rpc_url = os.getenv('POLYGON_RPC_URL')
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Adresse du portefeuille à surveiller (Remplacez par votre adresse publique)
WALLET_ADDRESS = "VOTRE_ADRESSE_PUBLIQUE_ICI"

def get_balances():
    if not w3.is_connected():
        print("Erreur : Impossible de se connecter au réseau Polygon.")
        return

    # Solde MATIC
    balance_wei = w3.eth.get_balance(WALLET_ADDRESS)
    balance_matic = w3.from_wei(balance_wei, 'ether')
    
    print(f"--- État de la Trésorerie GloirePay ---")
    print(f"Adresse : {WALLET_ADDRESS}")
    print(f"Solde MATIC : {balance_matic} MATIC")
    print(f"---------------------------------------")

if __name__ == "__main__":
    get_balances()
