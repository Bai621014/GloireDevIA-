import time
import sys
import os

# Ajoute le répertoire actuel (là où est orchestrator.py) au chemin
# Puis remonte d'un cran pour que 'src' soit vu comme un package
sys.path.append(os.getcwd())

from src.gloire_base import GloireBase
from src.blockchain_agent import GloireDevIA_Web3

class GloireOrchestrator:
    def __init__(self):
        self.db = GloireBase()
        self.agent = GloireDevIA_Web3()
        # Lecture du seuil
        self.threshold = self.db.db.get("settings", {}).get("minTreasuryThreshold", 1000000000000000000)

    def run_cycle(self):
        print(f"\n--- [GloirePay] Audit {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        try:
            status = self.agent.get_treasury_status()
            balance = status.get('balance_wei', 0)
            print(f"Trésorerie Actuelle : {balance} Wei")
            
            if int(balance) >= int(self.threshold):
                print("Action: Seuil atteint. Exécution maintenance...")
                result = self.agent.execute_treasury_maintenance()
                self.db.save_tx(f"MAIN-{int(time.time())}", {"action": "maintenance", "result": result})
                self.db.save_state()
            else:
                print("Action: Trésorerie protégée (sous seuil). Standby.")
        except Exception as e:
            print(f"Alerte Système : Erreur lors de l'audit -> {e}")

if __name__ == "__main__":
    bot = GloireOrchestrator()
    print("Système de surveillance activé sur Redmi 13.")
    while True:
        bot.run_cycle()
        print("Mise en veille (Prochain audit dans 1 heure)...")
        time.sleep(3600)
