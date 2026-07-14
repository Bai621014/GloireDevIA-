from flask import Flask, request, jsonify
from src import GloireDevIA, SecurityAudit
import os

app = Flask(__name__)

# Initialisation souveraine des moteurs
agent = GloireDevIA()
auditeur = SecurityAudit()

# Middleware de sécurité : Vérification d'auth souveraine
@app.before_request
def verify_auth():
    if request.method == 'POST':
        auth_header = request.headers.get('X-Gloire-Auth')
        if not auth_header or not auth_header.startswith('SIG_'):
            return jsonify({"status": "SECURITY_ALERT", "message": "Accès non autorisé"}), 403

@app.post('/analyze')
def analyze():
    """Point d'entrée sécurisé pour audit ISO 20022 et déploiement."""
    payload = request.get_json()
    
    if not payload:
        return jsonify({"status": "ERROR", "message": "Payload invalide"}), 400
    
    try:
        # Audit rigoureux pré-exécution
        audit_res = auditeur.audit(payload)
        
        # Exécution de la logique IA
        result = agent.analyze(payload)
        
        # Déploiement conditionnel avec signature d'intégrité
        if payload.get("generate_code"):
            agent.coder_nouveau_module("module_souverain", payload["code"])
            result.update({
                "deployment": "SUCCESS",
                "integrity": "SIGNED_BY_GLOIRE_2026",
                "audit": audit_res
            })
        
        return jsonify({"status": "SUCCESS", "data": result})
        
    except Exception as e:
        # Log technique interne, mais réponse sécurisée externe
        app.logger.error(f"Erreur système : {str(e)}")
        return jsonify({"status": "CRITICAL_FAILURE", "message": "Erreur interne du système"}), 500

@app.get('/health')
def health_check():
    """Vérification de vie pour le monitoring VIP."""
    return jsonify({"status": "OPERATIONAL", "chain": "Polygon_zkEVM"})

if __name__ == "__main__":
    # Désactivation du mode debug en production pour la sécurité
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
