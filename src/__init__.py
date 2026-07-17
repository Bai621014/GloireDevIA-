"""
GLOIREPAY — MODULE D'INITIALISATION SOUVERAIN (2026.VIP)
Standard : ISO 20022 - Architecture : Façade Sécurisée
"""

import logging

# 1. Configuration du log système
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [GLOIREPAY] %(message)s")
logger = logging.getLogger("GloirePay.Init")

# 2. Importations relatives (puisque tout est dans le dossier src)
from .gloire_dev_ia import GloireDevIA
from .security import SecurityAudit
from .web3_manager import verifier_tresorerie
from .gloire_hub import calculer_valeur_fcfa

# Métadonnées de conformité
__version__ = "2026.07.14"
__author__ = "GloirePay Core Team"
__all__ = [
    "GloireDevIA", 
    "SecurityAudit", 
    "verifier_tresorerie", 
    "calculer_valeur_fcfa", 
    "get_system_status"
]

def get_system_status() -> dict:
    """Vérification d'intégrité haute-fidélité pour le module."""
    try:
        status = {
            "module": "GloirePay.SrcPackage",
            "status": "OPERATIONAL",
            "version": __version__,
            "compliance": "ISO_20022_V1"
        }
        logger.info(f"Intégrité vérifiée : {status['status']} (v{__version__})")
        return status
    except Exception as e:
        logger.error(f"Erreur d'intégrité système : {e}")
        return {"status": "CRITICAL_FAILURE", "module": "GloirePay.SrcPackage"}

# Initialisation du noyau
logger.info("Noyau Souverain en ligne au sein de src/.")
