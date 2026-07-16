import os
import sys
from web3 import Web3

# Récupération sécurisée de l'URL depuis les variables d'environnement
rpc_url = os.getenv('POLYGON_RPC_URL')

# Initialisation du client Web3
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Adresse de votre Trésorerie Souveraine
WALLET_ADDRESS = "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d"

def get_balances():
    """Récupération de l'état de la trésorerie avec intégrité."""
    if not w3.is_connected():
        print(">>> [ERREUR] Impossible de se connecter au réseau Polygon zkEVM.")
        sys.exit(1)

    # Validation du checksum pour prévenir les erreurs de frappe
    checksum_address = Web3.to_checksum_address(WALLET_ADDRESS)

    # Solde MATIC (ou ETH sur zkEVM)
    balance_wei = w3.eth.get_balance(checksum_address)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    
    print(f"--- [GLOIREPAY] État de la Trésorerie ---")
    print(f"Adresse : {checksum_address}")
    print(f"Solde disponible : {balance_eth} ETH/MATIC")
    print(f"----------------------------------------")

if __name__ == "__main__":
    get_balances()
