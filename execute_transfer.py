import os
from web3 import Web3

def send_transaction():
    # 1. Récupération des secrets
    rpc_url = os.getenv('POLYGON_RPC_URL')
    raw_key = os.getenv('GLOBALE_CLE_PRIVEE')
    
    # 2. DEBUG : Diagnostic immédiat pour voir pourquoi la clé échoue
    if raw_key:
        print(f">>> [DEBUG] Longueur de la clé reçue : {len(raw_key)}")
        print(f">>> [DEBUG] Aperçu : {raw_key[:5]}...")
    else:
        print(">>> [DEBUG] ERREUR : La variable GLOBALE_CLE_PRIVEE est vide !")
    
    # 3. Vérification stricte
    if not rpc_url:
        raise ValueError("ERREUR : POLYGON_RPC_URL introuvable !")
    if not raw_key:
        raise ValueError("ERREUR : GLOBALE_CLE_PRIVEE introuvable !")

    # 4. Connexion au réseau
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # 5. Nettoyage ultra-robuste (filtre uniquement les caractères hexadécimaux)
    clean_key = "".join(c for c in raw_key if c in "0123456789abcdefABCDEF")
    print(f">>> [DEBUG] Longueur après nettoyage : {len(clean_key)}")
    
    # Tentative de chargement du compte
    try:
        account = w3.eth.account.from_key(clean_key)
    except Exception as e:
        raise ValueError(f"ERREUR : Clé privée invalide après nettoyage. Détail : {e}")
    
    to_address = "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d"
    
    print(f">>> [SOUVERAINETÉ] Envoi depuis {account.address} vers {to_address}")
    
    # 6. Construction et envoi de la transaction
    nonce = w3.eth.get_transaction_count(account.address)
    tx = {
        'nonce': nonce,
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
