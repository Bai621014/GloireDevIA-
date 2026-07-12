from src.blockchain_agent import GloireDevIA_Web3

def test_connectivity():
    print("--- Diagnostic GloireDevIA ---")
    agent = GloireDevIA_Web3()
    
    # Test 1: Connexion RPC
    is_connected = agent.w3.is_connected()
    print(f"Connexion au nœud zkEVM: {'OK' if is_connected else 'ECHEC'}")
    
    if is_connected:
        # Test 2: Lecture de la blockchain
        try:
            status = agent.get_treasury_status()
            print(f"Audit Trésorerie: {status['address']}")
            print(f"Solde récupéré: {status['balance_wei']} Wei")
        except Exception as e:
            print(f"Erreur lors de la lecture du contrat: {e}")

if __name__ == "__main__":
    test_connectivity()
