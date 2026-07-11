from flask import Flask, render_template, jsonify, request
from .gloire_dev_ia import GloireDevIA
from .security import SecurityAudit
import json

# Initialisation de Flask en précisant les dossiers
app = Flask(__name__, template_folder='templates', static_folder='static')

# Instancier l'agent et l'auditeur
agent = GloireDevIA()
auditor = SecurityAudit()

@app.route('/')
def index():
    return render_template('index.html', agent_name=agent.name)

@app.post('/analyze')
def analyze():
    # Accepte JSON envoyé par fetch ou formulaire
    if request.is_json:
        payload = request.get_json(silent=True) or {}
    else:
        raw = request.form.get('payload') or request.data.decode('utf-8')
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            payload = {"raw": raw}

    result = agent.analyze(payload)

    # Si la requête attend HTML, rendre un template, sinon JSON
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept:
        return render_template('result.html', title='Analyse', result=result)
    return jsonify(result)

@app.post('/audit')
def audit():
    if request.is_json:
        payload = request.get_json(silent=True) or {}
    else:
        raw = request.form.get('payload') or request.data.decode('utf-8')
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            payload = {"raw": raw}

    report = auditor.audit(payload)
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept:
        return render_template('result.html', title='Audit', result=report)
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
