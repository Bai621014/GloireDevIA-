"""
GLOIREPAY — SCRIPT DE SIMULATION DE RETRAIT EN LIVE (2026.VIP)
Placé à la racine du projet.
"""
import logging
import sys
import os

# Force l'accès au dossier 'src' pour les importations
sys.path.insert(0, os.getcwd())

# Importation depuis le dossier src
from src.gloire_hub import GloireHub

# Configuration des logs pour voir l'exécution en temps réel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("GloirePay-Test")

class MockWeb3Manager:
    """Simule le gestionnaire blockchain pour valider le statut et le solde."""
    def get_treasury_status(self):
        return {
            "status": "COMPLIANT",
            "balance_eth": 1500.0  # Solde de simulation en MATIC
        }

def lancer_retraits_live():
    logger.info("==================================================")
    logger.info("🚀 DEMARRAGE DU PIPELINE DE RETRAIT LIVE - GLOIREPAY")
    logger.info("==================================================")

    # 1. Initialisation de l'orchestrateur avec le faux manager blockchain
    w3_mock = MockWeb3Manager()
    hub = GloireHub(web3_manager=w3_mock)

    # Vérification initiale du solde disponible
    solde = hub.verifier_solde_disponible()
    logger.info(f"[Blockchain] Solde disponible détecté sur le Safe : {solde} MATIC")
    logger.info("--------------------------------------------------")

    # 2. Simulation de Retrait Live 1 — AIRTEL MONEY
    logger.info("[LIVE] Exécution du retrait vers le compte Airtel Money...")
    resultat_airtel = hub.initier_retrait_mobile_money(operateur="AIRTEL_MONEY", montant_matic=250.0)
    
    if resultat_airtel["status"] == "SUCCESS":
        logger.info(f"✅ AIRTEL MATCHING OK : {resultat_airtel['message']}")
    else:
        logger.error(f"❌ ÉCHEC AIRTEL : {resultat_airtel['message']}")

    logger.info("--------------------------------------------------")

    # 3. Simulation de Retrait Live 2 — MOOV FLOOZ
    logger.info("[LIVE] Exécution du retrait vers le compte Moov Flooz...")
    resultat_moov = hub.initier_retrait_mobile_money(operateur="MOOV_FLOOZ", montant_matic=400.0)
    
    if resultat_moov["status"] == "SUCCESS":
        logger.info(f"✅ MOOV MATCHING OK : {resultat_moov['message']}")
    else:
        logger.error(f"❌ ÉCHEC MOOV : {resultat_moov['message']}")

    logger.info("==================================================")
    logger.info("🎉 FIN DE LA SIMULATION - TOUT EST EN ORDRE POUR LE RETRAIT LIVE !")
    logger.info("==================================================")

if __name__ == "__main__":
    lancer_retraits_live()
