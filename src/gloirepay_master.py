import asyncio
from src.blockchain_agent import GloireDevIA_Web3
from src.gloire_hub import GloireHub # Votre moteur de conversion

class GloirePayMaster:
    """Orchestrateur souverain : Le Cerveau du système."""
    def __init__(self):
        self.agent = GloireDevIA_Web3() # Lien Blockchain
        self.hub = GloireHub()          # Logique IA/Conversion
        
    async def run_vip_cycle(self):
        """Cycle d'exécution haute performance."""
        # 1. Audit Sécurité
        if not self.agent.w3.is_connected():
            raise ConnectionError("Alerte Souveraine : Nœud déconnecté")
            
        # 2. Gestion Trésorerie avec GloireHub
        solde_wei = self.agent.get_treasury_status().get("balance_wei", 0)
        solde_matic = self.agent.w3.from_wei(solde_wei, 'ether')
        
        # 3. Conversion IA GloireHub (Maintenue)
        valeur_fiat = self.hub.convertir_monnaie_globale(float(solde_matic), "MATIC", "EUR")
        
        print(f"[GloirePay] État : {valeur_fiat:.2f} EUR en trésorerie sécurisée.")
        
        # 4. Fonction n°3 : Alerte de seuil critique (Phase 1)
        if float(solde_matic) < 1.0: # Seuil VIP
            print("[ALERTE] Trésorerie sous seuil souverain. Action requise.")
            # Ici, déclenchement Webhook/Alerte
        
        return True

# --- EXÉCUTION ---
if __name__ == "__main__":
    master = GloirePayMaster()
    asyncio.run(master.run_vip_cycle())
