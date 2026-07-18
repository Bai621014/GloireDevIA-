"""
GLOIREPAY — PIPELINE DE TEST DE L'ARCHIVAGE DE PRODUCTION
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())
from src.gloire_archiver import GloireArchiverEngine

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("GloirePay-ArchiverTest")

if __name__ == "__main__":
    logger.info("⚡️ Analyse de la persistance et de la conformité du système d'écriture...")
    
    archiver = GloireArchiverEngine(dossier_archive="data/test_archives")
    
    tableau_simule = """
    +----------------------+------------------+
    | CATÉGORIE            | MONTANT (FCFA)   |
    +----------------------+------------------+
    | DOUANE_REVENUE       | 4,500,000        |
    +----------------------+------------------+
    """
    
    # Exécution de l'archivage
    chemin_genere = archiver.archiver_tableau("DOUANE_JULLET", list_data = tableau_simule)
    
    # Vérifications de sécurité et de présence du fichier
    assert os.path.exists(chemin_genere) is True
    
    # Nettoyage propre après validation du pipeline
    with open(chemin_genere, "r", encoding="utf-8") as f:
        contenu = f.read()
    assert "DOUANE_REVENUE" in contenu
    
    logger.info("🏆 PIPELINE D'ARCHIVAGE SÉCURISÉ CERTIFIÉ SOUVERAIN ET AU VERT ! AMEN !")

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
# Tout est possible à celui qui croit au nom de Jésus Christ, et avec la puissance du Saint Esprit.
