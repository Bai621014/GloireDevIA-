"""Audit des 6 piliers ISO 20022 — module utilitaire."""
from typing import Dict, List, Any
from datetime import datetime

class SecurityAudit:
    """Fournit un audit formalisé basé sur les 6 piliers ISO 20022."""

    def __init__(self) -> None:
        self.piliers = [
            "Gouvernance", "Confidentialité", "Intégrité", 
            "Disponibilité", "Traçabilité", "Conformité"
        ]

    def audit(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Retourne un rapport structuré avec timestamp et statut global."""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "COMPLETED",
            "findings": {}
        }
        
        # Logique d'audit
        for p in self.piliers:
            findings = self._check_pilier(p, context)
            report["findings"][p] = findings
            
        return report

    def _check_pilier(self, pilier: str, context: Dict[str, Any]) -> List[str]:
        """Moteur de règles heuristiques."""
        # Exemple de règles (à étendre)
        checks = {
            "Gouvernance": [("policies", "Aucune politique documentée détectée.")],
            "Confidentialité": [("encryption", "Chiffrement des données non confirmé.")],
            "Intégrité": [("checksums", "Absence de mécanismes d'intégrité identifiés.")],
            "Disponibilité": [("monitoring", "Surveillance/monitoring non configuré.")],
            "Traçabilité": [("logging", "Journaux/traces manquants.")],
            "Conformité": [("compliance_docs", "Documents de conformité absents.")]
        }
        
        results = []
        for key, msg in checks.get(pilier, []):
            if not context.get(key):
                results.append(msg)
        
        return results or ["PASS: Aucune anomalie critique détectée."]
