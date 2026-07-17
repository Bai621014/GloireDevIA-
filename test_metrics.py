"""
GLOIREPAY — PIPELINE DE TEST DES STATISTIQUES DE PRODUCTION
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())
from src.gloire_metrics import GloireMetricsEngine

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("GloirePay-MetricsTest")

if __name__ == "__main__":
    logger.info("⚡️ Analyse de la vélocité et de la précision du moteur de métriques...")
    
    moteur = GloireMetricsEngine()
    
    # Simulation de 2 transactions : 1 réussite de 500 000 FCFA et 1 échec
    moteur.enregistrer_transaction_metrique("COMPLIANT", 500000.0)
    moteur.enregistrer_transaction_metrique("FAILED", 150000.0)
    
    rapport = moteur.generer_rapport_performance()
    
    # Vérifications techniques
    assert rapport["total_enregistre"] == 2
    assert rapport["volume_global_fcfa"] == 500000.0
    assert rapport["taux_succes_pourcentage"] == 50.0
    
    logger.info("🏆 PIPELINE DE STATISTIQUES FINANCIÈRES CERTIFIÉ AU VERT ! AMEN !")

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
# Tout est possible à celui qui croit au nom de Jésus Christ, et avec la puissance du Saint Esprit.
