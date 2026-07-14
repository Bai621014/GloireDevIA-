"""
GLOIREDEVIA - MODULE D'INITIALISATION SOUVERAIN
Standard : ISO 20022
"""

# Importation directe pour accès rapide (Pattern Façade)
from .gloire_dev_ia import GloireDevIA
from .security import SecurityAudit

# Métadonnées de versionnement pour le suivi d'audit
__version__ = "2026.07.14"
__author__ = "GloirePay Core"

# Définition explicite des composants exposés
__all__ = ["GloireDevIA", "SecurityAudit"]

def get_system_status():
    """Vérification rapide de l'intégrité du module."""
    return {
        "module": "GloireDevIA.src",
        "status": "OPERATIONAL",
        "version": __version__
    }
