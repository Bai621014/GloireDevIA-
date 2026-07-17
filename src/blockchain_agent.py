"""
GLOIREPAY — GESTIONNAIRE WEB3 SOUVERAIN (2026.VIP)
"""

import logging
from datetime import datetime, timezone
from web3 import Web3

# Import compatible v5 et v6
try:
    from web3.middleware.geth_poa_middleware import geth_poa_middleware # web3 >= 6
except ImportError:
    from web3.middleware import geth_poa_middleware # web3 == 5

# Configuration du logger pour audit permanent
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [WEB3-VIP] %(message)s")
logger = logging.getLogger("GloirePay-VIP")

class GloireWeb3Manager:
    """Gestionnaire souverain de fonds et d'audit blockchain (Version Pro VIP)."""
    
    def __init__(self, provider_url: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Injection du middleware PoA indispensable pour zkEVM
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Registre des contrats souverains
        self.registry = {
            "contracts": {
                "Treasury": Web3.to_checksum_address("0xA1e615A74D22D9dC3D9388c2b5009DAc7917784d")
            }
        }
        logger.info("[SYSTEM] Gestionnaire Web3 initialisé avec succès.")

    def estimate_maintenance_cost(self) -> int:
        try:
            if not self.w3.is_connected():
                raise ConnectionError("Nœud RPC indisponible")
            gas_price = self.w3.eth.gas_price
            estimated_wei = int(gas_price * 200000 * 1.2)
            logger.info(f"[Audit] Coût maintenance estimé : {estimated_wei} Wei")
            return estimated_wei
        except Exception as e:
            logger.error(f"[Audit] Erreur critique estimation Gas : {e}")
            raise 

    def get_treasury_status(self) -> dict:
        try:
            treasury_addr = self.registry['contracts'].get('Treasury')
            if not Web3.is_checksum_address(treasury_addr):
                raise ValueError("Intégrité adresse échouée : Checksum invalide")
            balance = self.w3.eth.get_balance(treasury_addr)
            return {
                "status": "COMPLIANT",
                "address": treasury_addr, 
                "balance_wei": balance, 
                "balance_eth": float(self.w3.from_wei(balance, 'ether')),
                "audit_timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"[Audit] Erreur accès Trésorerie : {e}")
            return {"status": "CRITICAL_FAILURE", "message": str(e)}
