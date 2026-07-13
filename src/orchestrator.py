import time
import sys
import os
from datetime import datetime

# Ajout du répertoire courant au PATH pour localiser le dossier 'src'
sys.path.append(os.getcwd())

# Importations absolues
from src.gloire_base import GloireBase
from src.blockchain_agent import GloireDevIA_Web3

class GloireOrchestrator:
    def __init__(self):
        self.db = GloireBase()
        self.agent = GloireDevIA_Web3()
        # Récupération du seuil avec valeur par défaut
        self.threshold = int(self.db.db.get("settings", {}).get("minTreasuryThreshold", 1000000000000000000))
        print(">>> [GloireDevIA-Pro] Initialisation terminée.")

    def run_cycle(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n--- [GloirePay] Audit {timestamp} ---")
        try:
            status = self.agent.get_treasury_status()
            balance = int(status.get('balance_wei', 0))
            print(f"Trésorerie Actuelle : {balance} Wei")
            
            if balance >= self.threshold:
                print(">> [Action] Seuil atteint. Exécution maintenance...")
                result = self.agent.execute_treasury_maintenance()
                self.db.save_tx(f"MAIN-{int(time.time())}", {"action": "maintenance", "result": result})
                self.db.save_state()
            else:
                print(">> [Standby] Trésorerie sécurisée (sous seuil).")
        except Exception as e:
            print(f"!! [CRITIQUE] : {str(e)}")

if __name__ == "__main__":
    bot = GloireOrchestrator()
    print("Système de surveillance activé.")
    while True:
        bot.run_cycle()
        time.sleep(3600)
