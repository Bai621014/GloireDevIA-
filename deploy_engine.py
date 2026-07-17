import sys
import os

# Importation directe depuis la racine (structure plate)
# On utilise les noms de fichiers exacts vus sur votre capture
from web3_manager import verifier_tresorerie
from gloire_hub import calculer_valeur_fcfa 

def run_gloiretech():
    print("--- [GloireTech] Initialisation Souveraine ---")
    
    try:
        # 1. Audit rapide du Gnosis Safe
        print("Audit du Safe en cours...")
        solde = verifier_tresorerie()
        
        # 2. Conversion intelligente via GloireHub
        print("Calcul de la valeur souveraine en FCFA...")
        valeur_fcfa = calculer_valeur_fcfa(solde)
        
        # 3. Rapport Pro VIP
        print(f"--- RAPPORT DE TRÉSORERIE ---")
        print(f"Solde actuel : {solde} MATIC")
        print(f"Valeur estimée : {valeur_fcfa} FCFA")
        print("Système stable : Prêt pour déploiement automatique.")
        
    except Exception as e:
        print(f"Erreur lors de l'exécution souveraine : {e}")
        # On affiche le détail de l'erreur pour le debug dans GitHub
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_gloiretech()
