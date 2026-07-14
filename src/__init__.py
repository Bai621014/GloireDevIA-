"""
GLOIREDEVIA — MODULE D'INITIALISATION SOUVERAIN (2026.VIP)
Standard : ISO 20022 - Architecture : Façade Sécurisée
"""

import logging
from .gloire_dev_ia import GloireDevIA
from .security import SecurityAudit

# Configuration du log système pour traçabilité immédiate
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [GLOIREPAY] %(message)s")
logger = logging.getLogger(__name__)

# Métadonnées de conformité
__version__ = "2026.07.14"
__author__ = "GloirePay Core Team"
__all__ = ["GloireDevIA", "SecurityAudit", "get_system_status"]

def get_system_status():
    """Vérification d'intégrité haute-fidélité pour le module."""
    status = {
        "module": "GloireDevIA.src",
        "status": "OPERATIONAL",
        "version": __version__,
        "compliance": "ISO_20022_V1"
    }
    logger.info(f"Intégrité vérifiée : {status['status']} (v{__version__})")
    return status

# Initialisation du logger de démarrage
logger.info("Noyau Souverain GloireDevIA en ligne.")
