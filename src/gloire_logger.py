"""
GLOIREPAY — SYSTÈME DE JOURNALISATION ET AUDIT PROFESSIONNEL (2026.VIP)
"""
import os
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger("GloirePay-Audit")

class GloireAuditLogger:
    """Gestionnaire souverain des journaux d'audit de transactions pour GloirePay."""
    
    def __init__(self, log_filename="data/transactions_audit.json"):
        self.log_filepath = log_filename
        # Création automatique du dossier de données s'il n'existe pas
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)
        logger.info(f"[AUDIT] Registre d'audit initialisé dans : {self.log_filepath}")

    def enregistrer_transaction(self, id_tx: str, operateur: str, destination: str, montant: float, statut: str) -> bool:
        """Enregistre un événement de transaction dans le fichier d'audit sécurisé."""
        evenement = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "transaction_id": id_tx,
            "operateur": operateur.upper(),
            "destination_telephone": destination,
            "montant_fcfa": montant,
            "statut_execution": statut.upper()
        }
        
        try:
            historique = []
            if os.path.exists(self.log_filepath) and os.path.getsize(self.log_filepath) > 0:
                with open(self.log_filepath, "r", encoding="utf-8") as f:
                    historique = json.load(f)
            
            historique.append(evenement)
            
            with open(self.log_filepath, "w", encoding="utf-8") as f:
                json.dump(historique, f, ensure_ascii=False, indent=4)
                
            logger.info(f"💾 [AUDIT-SUCCÈS] Transaction {id_tx} sauvegardée dans le registre.")
            return True
        except Exception as e:
            logger.error(f"❌ [AUDIT-ERREUR] Échec de l'écriture du journal : {str(e)}")
            return False
