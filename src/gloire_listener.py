"""
GLOIREPAY — MODULE D'ÉCOUTE ET DE LECTURE DES ORDRES DU BOSS (2026.VIP)
"""
import os
import logging

logger = logging.getLogger("GloirePay-Listener")

class GloireInstructionsListener:
    """Moteur chargé de lire le fichier d'instructions laissé par le Boss."""

    def __init__(self, chemin_fichier: str = "instructions.txt"):
        self.chemin_fichier = chemin_fichier

    def lire_et_executer_ordres(self) -> str:
        """Ouvre le fichier texte, extrait les ordres et les transmet à l'Agent."""
        if not os.path.exists(self.chemin_fichier):
            logger.info("ℹ️ Aucun nouveau fichier d'instructions détecté. L'Agent reste en veille.")
            return "En veille active. Tout est vert !"

        logger.info(f"⚡️ [LISTENER] Détection d'ordres souverains dans {self.chemin_fichier}...")
        
        with open(self.chemin_fichier, "r", encoding="utf-8") as f:
            ordres = f.read()

        logger.info("🤖 [AGENT-ACTION] Ordres lus avec succès ! Lancement de l'exécution automatique...")
        return ordres

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
