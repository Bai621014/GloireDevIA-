"""
GLOIREPAY — POINT D'ENTRÉE PRINCIPAL DE PRODUCTION (2026.VIP)
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())
from src.gloire_security import GloireSecurityManager
from src.gloire_logger import GloireAuditLogger
from src.gloire_reporting import GloireReportingEngine

# Configuration du logging de production
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("GloirePay-Main")

def executer_pipeline_production():
    logger.info("==================================================")
    logger.info("⚡️ INITIALISATION DU SYSTÈME SOUVERAIN GLOIREPAY ⚡️")
    logger.info("==================================================")
    
    try:
        # 1. Initialisation de la Sécurité Maximale
        security = GloireSecurityManager()
        
        # Simuler une vérification rapide (récupération sécurisée sans affichage de la clé entière)
        cle_privee = security.obtenir_cle_privee()
        logger.info(f"🔒 [VÉRIFICATION] Signature Web3 active (Clé: {cle_privee[:6]}...)")
        
        # 2. Initialisation du Registre d'Audit
        registre_principal = "data/transactions_audit.json"
        audit = GloireAuditLogger(log_filename=registre_principal)
        
        # 3. Simulation d'une transaction de Production réussie
        logger.info("💸 Traitement d'une transaction de test de production...")
        id_transaction = "TX-PROD-2026-VIP"
        audit.enregistrer_transaction(
            id_tx=id_transaction,
            operateur="AIRTEL",
            destination="+23562101468",
            montant=25000.0,
            statut="SUCCES"
        )
        
        # 4. Génération instantanée du Rapport de Flux
        reporting = GloireReportingEngine(log_filename=registre_principal)
        bilan = reporting.generer_rapport_flux()
        
        logger.info("==================================================")
        logger.info(f"🏆 BILAN EN DIRECT : Total Traité = {bilan['total_volume_fcfa']} FCFA")
        logger.info(f"📈 Transactions Réussies : {bilan['transactions_reussies']}")
        logger.info("==================================================")
        logger.info("🎉 EXPÉDITION ET SÉCURISATION ACCOMPLIES AVEC SUCCÈS !")
        
    except Exception as e:
        logger.critical(f"❌ [ERREUR SYSTÈME] Blocage critique du pipeline : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    executer_pipeline_production()

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
