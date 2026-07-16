from flask import Flask, request, jsonify
from src.blockchain_agent import GloireWeb3Manager
from src.gloire_hub import GloireHub
from src.orchestrator import GloireBase, GloireCoin
import os

app = Flask(__name__)

# Initialisation du cœur souverain (Injection de dépendances)
w3_manager = GloireWeb3Manager("https://zkevm-rpc.com")
db = GloireBase()
ledger = GloireCoin()
hub = GloireHub(db, ledger, w3_manager)

# --- ROUTES API ---
@app.before_request
def verify_auth():
    if request.method == 'POST':
        auth_header = request.headers.get('X-Gloire-Auth')
        if not auth_header or not auth_header.startswith('SIG_'):
            return jsonify({"status": "SECURITY_ALERT", "message": "Accès refusé"}), 403

@app.post('/swap')
def trigger_swap():
    """Point d'entrée VIP pour swap souverain."""
    data = request.get_json()
    try:
        # Appel au hub déjà initialisé
        result = hub.swap(data['amount'], data['pair'])
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.get('/health')
def health():
    return jsonify({"status": "OPERATIONAL", "chain": "Polygon_zkEVM", "timestamp": "2026.VIP"})

# --- INITIALISATION SYSTÈME ---
if __name__ == "__main__":
    print(">>> GLOIREPAY INITIALISATION SOUVERAINE...")
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
