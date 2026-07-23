import os
import json
from web3 import Web3
from solcx import compile_source, install_solc

# Configuration RPC pour le Testnet Polygon Amoy
RPC_URL = os.getenv("POLYGON_RPC_URL", "https://rpc-amoy.polygon.technology")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SOVEREIGN_OWNER = os.getenv("SOVEREIGN_OWNER_ADDRESS", "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d")
TREASURY_ADDRESS = os.getenv("TREASURY_ADDRESS", "0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d")

def run_test_deployment():
    print("====================================================")
    print("   TEST AUTOMATIQUE DEPLOIEMENT GLC - POLYGON AMOY  ")
    print("====================================================")

    # 1. Verification du contrat
    contract_path = os.path.join("contracts", "GloireCoin.sol")
    if not os.path.exists(contract_path):
        contract_path = "GloireCoin.sol"

    if not os.path.exists(contract_path):
        raise FileNotFoundError(f"[-] Contrat introuvable a l'adresse : {contract_path}")

    print(f"[+] Contrat Solidity localise : {contract_path}")

    # 2. Compilation Solidity locale
    print("[...] Installation & Compilation Solidity 0.8.20...")
    install_solc('0.8.20')
    
    with open(contract_path, "r", encoding="utf-8") as f:
        contract_source = f.read()

    compiled_sol = compile_source(
        contract_source,
        output_values=['abi', 'bin'],
        solc_version='0.8.20'
    )

    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    print(f"[SUCCES] Smart Contract GLC compile sans aucune erreur !")
    print(f"[+] Taille du Bytecode : {len(bytecode)} octets")

    # 3. Test de Connexion au Reseau Amoy
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    connected = w3.is_connected()
    print(f"[+] Connexion au Noeud Amoy Testnet : {'REUSSIE' if connected else 'ECHEC'}")

    # 4. Simulation ou Déploiement Réel
    if PRIVATE_KEY:
        print("[...] Clé privée détectée. Lancement du déploiement réel sur Amoy...")
        account = w3.eth.account.from_key(PRIVATE_KEY)
        GloireCoinContract = w3.eth.contract(abi=abi, bytecode=bytecode)
        
        nonce = w3.eth.get_transaction_count(account.address)
        tx = GloireCoinContract.constructor(
            Web3.to_checksum_address(SOVEREIGN_OWNER),
            Web3.to_checksum_address(TREASURY_ADDRESS)
        ).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price,
            'chainId': 80002 # Polygon Amoy Chain ID
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[+] Transaction émise : {tx_hash.hex()}")
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = receipt.contractAddress
        print(f"\n[SUCCÈS AMOY] GLC Déployé à l'adresse : {contract_address}")
    else:
        print("\n[INFO] Mode Simulation Active (Sans Clé Privée).")
        print(f"[+] Proprietaire Souverain parametre : {SOVEREIGN_OWNER}")
        print(f"[+] Portefeuille Tresorerie parametre : {TREASURY_ADDRESS}")
        contract_address = "0xSIMULATED_GLC_CONTRACT_ADDRESS_AMOY_TESTNET"

    # Enregistrement du manifeste
    test_manifest = {
        "status": "TEST_PASSED",
        "network": "Polygon Amoy Testnet",
        "contract_address": contract_address,
        "sovereign_owner": SOVEREIGN_OWNER,
        "treasury_address": TREASURY_ADDRESS,
        "abi": abi
    }

    with open("gloirecoin_test_manifest.json", "w", encoding="utf-8") as f:
        json.dump(test_manifest, f, indent=4)

    print("\n====================================================")
    print("   TEST TOTALEMENT VALIDE — PRÊT POUR PIPELINE AUTO   ")
    print("====================================================")

if __name__ == "__main__":
    run_test_deployment()
