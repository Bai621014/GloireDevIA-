"""
GLOIREPAY — TEST DE CONNECTIVITÉ SOUVERAIN (2026.VIP)
Diagnostic haute performance pour nœud Polygon zkEVM.
"""

import sys
from pathlib import Path
import logging

# Configuration logging souverain
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("GloirePay-Diagnostic")

# Injection du PATH pour robustesse absolue
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.blockchain_agent import GloireDevIA_Web3

def run_diagnostic():
    """Diagnostic complet de l'agent Web3."""
    logger.info("--- DÉBUT DIAGNOSTIC SOUVERAIN ---")
    
    try:
        agent = GloireDevIA_Web3()
        
        # Test 1: Intégrité connexion RPC
        if not agent.w3.is_connected():
            logger.error("Connexion au nœud zkEVM : ÉCHEC")
            return
        
        logger.info(f"Connexion au nœud zkEVM : OK (Provider: {agent.w3.provider.endpoint_uri})")
        
        # Test 2: Validation Chain ID (Standard Web3)
        chain_id = agent.w3.eth.chain_id
        logger.info(f"Réseau détecté (ChainID): {chain_id}")
        
        # Test 3: Audit de trésorerie souveraine
        status = agent.get_treasury_status()
        
        if status.get("status") == "online":
            logger.info(f"Audit Trésorerie : {status['address']} (VALIDÉ)")
            logger.info(f"Solde disponible : {status['balance_wei']} Wei")
        else:
            logger.warning(f"Audit Trésorerie : ERREUR ({status.get('message')})")
            
    except Exception as e:
        logger.critical(f"Erreur système critique : {e}")
    finally:
        logger.info("--- FIN DIAGNOSTIC SOUVERAIN ---")

if __name__ == "__main__":
    run_diagnostic()
