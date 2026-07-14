from flask import Flask, request, jsonify
from src import GloireDevIA, SecurityAudit # Utilisation du pattern Façade

app = Flask(__name__)

# Initialisation souveraine
agent = GloireDevIA()
auditeur = SecurityAudit()

@app.post('/analyze')
def analyze():
    """Point d'entrée sécurisé pour l'analyse et déploiement IA."""
    payload = request.get_json()
    
    # 1. Validation souveraine de la requête
    if not payload:
        return jsonify({"status": "ERROR", "message": "Payload vide"}), 400
    
    try:
        # 2. Audit de sécurité pré-exécution
        audit_res = auditeur.audit(payload)
        
        # 3. Exécution de l'IA
        result = agent.analyze(payload)
        
        # 4. Déploiement souverain conditionnel
        if payload.get("generate_code"):
            agent.coder_nouveau_module("nouveau_module", payload["code"])
            result["log"] = "Module déployé souverainement par GloireDevIA."
            result["integrity"] = "SIGNED_BY_GLOIRE"
        
        return jsonify({"status": "SUCCESS", "data": result, "audit": audit_res})
        
    except Exception as e:
        return jsonify({"status": "CRITICAL_FAILURE", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
