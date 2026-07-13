import time
import sys
import os
from datetime import datetime

# Ajoute le répertoire courant (la racine) au PATH
sys.path.append(os.getcwd())

# Importation absolue (SANS LES POINTS)
from src.gloire_base import GloireBase
from src.blockchain_agent import GloireDevIA_Web3

class GloireOrchestrator:
    def __init__(self):
        self.db = GloireBase()
        self.agent = GloireDevIA_Web3()
        self.threshold = int(self.db.db.get("settings", {}).get("minTreasuryThreshold", 10**18))
        print(">>> [GloireDevIA-Pro] Initialisation terminée.")

    def run_cycle(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n--- [GloirePay] Audit {timestamp} ---")
        try:
            status = self.agent.get_treasury_status()
            balance = int(status.get('balance_wei', 0))
            print(f"Trésorerie Actuelle : {balance / 10**18:.6f} ETH")
            if balance >= self.threshold:
                print(">> [Action] Maintenance souveraine déclenchée.")
                result = self.agent.execute_treasury_maintenance()
                self.db.save_tx(f"MAIN-{int(time.time())}", {"status": "SUCCESS", "result": result})
                self.db.save_state()
            else:
                print(">> [Standby] Trésorerie sécurisée.")
        except Exception as e:
            print(f"!! [CRITIQUE] : {str(e)}")

if __name__ == "__main__":
    bot = GloireOrchestrator()
    print("Système de surveillance activé sur Redmi 13.")
    while True:
        bot.run_cycle()
        time.sleep(3600)
