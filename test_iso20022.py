"""
GLOIREPAY — PIPELINE DE TEST DE CONFORMITÉ ISO 20022
"""
import os
import sys
import logging

sys.path.insert(0, os.getcwd())
# On importe le validateur que vous venez de coller
from gloire_audit_iso import ISO20022_Validator  # Ajustez le nom de l'import selon le nom exact de votre fichier précédent

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("GloirePay-ISOTest")

if __name__ == "__main__":
    logger.info("⚡️ Début de l'audit de conformité bancaire globale ISO 20022...")
    
    # Scénario 1 : Transaction Parfaite (Doit passer COMPLIANT)
    tx_valide = {
        "sender": "0xA1eB777Souverain",
        "receiver": "+23562101468",
        "amount": 250000.0,
        "currency": "XAF",
        "purpose": "Achat Équipement AJEDIP"
    }
    rapport_valide = ISO20022_Validator.audit_transaction(tx_valide)
    assert rapport_valide["status"] == "COMPLIANT"
    assert "tx_hash" in rapport_valide
    logger.info("✅ Test 1 : Transaction légitime validée avec succès.")

    # Scénario 2 : Transaction Fraude/Erreur (Montant négatif - Doit être rejeté)
    tx_invalide_montant = {
        "sender": "0xA1eB777Souverain",
        "receiver": "+23590784260",
        "amount": -5000.0,
        "currency": "XAF",
        "purpose": "Faux Transfert"
    }
    rapport_invalide = ISO20022_Validator.audit_transaction(tx_invalide_montant)
    assert rapport_invalide["status"] == "NON-COMPLIANT"
    logger.info("✅ Test 2 : Tentative de montant négatif bloquée avec succès.")

    # Scénario 3 : Structure Incomplète (Champs obligatoires manquants - Doit échouer)
    tx_incomplete = {
        "sender": "0xA1eB777Souverain",
        "amount": 10000.0
    }
    rapport_incomplet = ISO20022_Validator.audit_transaction(tx_incomplete)
    assert rapport_incomplet["status"] == "NON-COMPLIANT"
    logger.info("✅ Test 3 : Structure incomplète rejetée avec succès.")

    logger.info("🏆 MOTEUR DE VALIDATION ISO 20022 CERTIFIÉ À 100% AU VERT ! AMEN !")

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
# Tout est possible à celui qui croit au nom de Jésus Christ, et avec la puissance du Saint Esprit.
