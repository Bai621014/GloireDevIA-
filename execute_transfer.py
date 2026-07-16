import os
from web3 import Web3

def send_transaction():
    # Connexion
    w3 = Web3(Web3.HTTPProvider(os.getenv('POLYGON_RPC_URL')))
    
    # Configuration sécurisée
    account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))
    to_address = "ADRESSE_DESTINATAIRE_ICI"
    
    # Préparation de la transaction
    tx = {
        'nonce': w3.eth.get_transaction_count(account.address),
        'to': to_address,
        'value': w3.to_wei(0.001, 'ether'), # Montant à envoyer
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 137 # 137 pour Polygon Mainnet, ajuster si besoin
    }
    
    # Signature et envoi
    signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f">>> [TRANSACTION] Hash : {w3.to_hex(tx_hash)}")

if __name__ == "__main__":
    send_transaction()
