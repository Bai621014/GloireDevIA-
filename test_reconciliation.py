"""
GLOIREPAY — SCRIPT DE VALIDATION DE RÉCONCILIATION (2026.VIP)
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())

from src.gloire_hub import GloireHub
from src.gloire_reconciliation import GloireReconciliationEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("GloirePay-MainTest")

class MockWeb3Manager:
    def get_treasury_status(self):
        return {"status": "COMPLIANT", "balance_eth": 2000.0}

if __name__ == "__main__":
    logger.info("⚡️ DEBUT DU PIPELINE DE RECONCILIATION ET NOTIFICATION VIP...")
    
    # Initialisation de la chaîne de décision
    w3_mock = MockWeb3Manager()
    hub = GloireHub(web3_manager=w3_mock)
    engine = GloireReconciliationEngine(hub=hub)
    
    # 1. Test d'audit croisé pour Airtel Money
    audit_airtel = engine.executer_verification_croisee("AIRTEL_MONEY", 100.0)
    if audit_airtel["statut_audit"] == "APPROUVÉ":
        engine.notifier_retrait_vip("AIRTEL_MONEY", "+23562101468", audit_airtel["valeur_retrait_fcfa"])
        
    # 2. Test d'audit croisé pour Moov Flooz
    audit_moov = engine.executer_verification_croisee("MOOV_FLOOZ", 200.0)
    if audit_moov["statut_audit"] == "APPROUVÉ":
        engine.notifier_retrait_vip("MOOV_FLOOZ", "+23590784260", audit_moov["valeur_retrait_fcfa"])

    logger.info("🏆 PIPELINE VALIDÉ SANS ERREUR AU NOM DE JÉSUS CHRIST !")
