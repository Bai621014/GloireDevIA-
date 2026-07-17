"""
GLOIREPAY — TEST DE SÉCURITÉ VIP FAST-PIPELINE
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())
from src.gloire_security import GloireSecurityManager

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("GloirePay-SecurityTest")

if __name__ == "__main__":
    logger.info("⚡️ Initialisation de l'audit de sécurité...")
    
    # Injection temporaire de clés de test pour simuler le pipeline GitHub Actions
    os.environ["GLOIRE_PRIVATE_KEY"] = "0x777SOUVERAINVIPJESUSCHRIST000000000000"
    os.environ["AIRTEL_API_SECRET"] = "SEC_AIRTEL_TCHAD_2026"
    os.environ["MOOV_API_SECRET"] = "SEC_MOOV_TCHAD_2026"
    
    # Exécution du gestionnaire de sécurité
    security = GloireSecurityManager()
    
    # Vérification des accès
    assert "0x777" in security.obtenir_cle_privee()
    assert "SEC_AIRTEL" in security.obtenir_secret_telecom("AIRTEL")
    
    logger.info("🏆 CADENASSAGE ENVIRO-MENTAL VALIDÉ AU VERT EN TOUTE SÉCURITÉ ! AMEN !")
