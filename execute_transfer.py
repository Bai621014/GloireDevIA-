import os
from web3 import Web3

def send_transaction():
    # Utilisation de la clé définie dans GitHub Secrets
    rpc_url = os.getenv('ALCHEMY_API_KEY') 
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Correction : Utilisation du nom exact de la variable secrète
    raw_key = os.getenv('POLYGON_PRIVATE_KEY')
    
    if not raw_key:
        raise ValueError("La clé privée n'est pas chargée. Vérifiez le nom de la variable dans GitHub Secrets.")

    clean_key = raw_key.strip().replace('0x', '')
    account = w3.eth.account.from_key(clean_key)
    
    to_address = "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d"
    
    print(f">>> [SOUVERAINETÉ] Envoi depuis {account.address} vers {to_address}")
    
    tx = {
        'nonce': w3.eth.get_transaction_count(account.address),
        'to': to_address,
        'value': w3.to_wei(0.0001, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 137
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, clean_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f">>> [TRANSACTION] Succès ! Hash : {w3.to_hex(tx_hash)}")

if __name__ == "__main__":
    send_transaction()
