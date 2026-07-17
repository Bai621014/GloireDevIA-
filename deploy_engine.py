import sys
import os
import json
import logging
import traceback

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [DEPLOY] %(message)s")
logger = logging.getLogger("DeployEngine")

# Force le répertoire racine dans le path
sys.path.insert(0, os.getcwd())

def run_deployment():
    """Moteur de déploiement souverain : Audit et Calcul de valeur."""
    logger.info("--- [GloireTech] Initialisation Souveraine ---")
    
    try:
        # 1. Chargement de la configuration
        if not os.path.exists('registry.json'):
            raise FileNotFoundError("Le fichier registry.json est manquant à la racine.")
            
        with open('registry.json', 'r') as f:
            config = json.load(f)
        logger.info(f"Connexion au réseau : {config['metadata']['network']}")
        
        # 2. Importations depuis src
        from src.web3_manager import verifier_tresorerie
        from src.gloire_hub import calculer_valeur_fcfa
        
        # 3. Exécution de l'audit critique
        logger.info("Audit du Safe et calcul de la valeur souveraine...")
        solde = verifier_tresorerie()
        valeur_fcfa = calculer_valeur_fcfa(solde)
        
        # 4. Rapport Final
        logger.info(f"--- RAPPORT DE TRÉSORERIE ---")
        logger.info(f"Solde actuel : {solde} MATIC")
        logger.info(f"Valeur estimée : {valeur_fcfa} FCFA")
        logger.info("Déploiement terminé avec succès.")
        
    except Exception as e:
        logger.error(f"Échec critique du déploiement : {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_deployment()
