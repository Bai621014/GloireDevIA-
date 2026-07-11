"""API Flask minimale exposant l'agent et l'audit."""

from flask import Flask, jsonify, request
from .gloire_dev_ia import GloireDevIA
from .security import SecurityAudit

app = Flask(__name__)
agent = GloireDevIA()
auditor = SecurityAudit()

@app.get("/")
def index():
    """Point d'entrée racine : redirige ou informe que le service est actif"""
    return jsonify({
        "status": "online",
        "message": "Bienvenue sur GloireDevIA API",
        "health_check": "/health"
    }), 200

@app.get("/health")
def health():
    return jsonify({"status": "ok", "agent": agent.name}), 200

@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    result = agent.analyze(payload)
    return jsonify(result), 200

@app.post("/audit")
def audit():
    payload = request.get_json(silent=True) or {}
    report = auditor.audit(payload)
    return jsonify(report), 200

if __name__ == "__main__":
    # Exécution locale pour développement (gunicorn utilisé en production sur Render)
    app.run(host="0.0.0.0", port=5000, debug=True)
