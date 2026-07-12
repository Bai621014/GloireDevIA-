/**
 * GLOIREPAY - MOTEUR INTERFACE ISO 20022
 * Version : 2026.07.12
 * Interface sécurisée pour l'audit et la conversion souveraine.
 */

const $ = sel => document.querySelector(sel);
const payloadEl = $('#payload');
const outEl = $('#output');
const btnA = $('#btnAnalyze');
const btnAudit = $('#btnAudit');

// Logique de conformité ISO 20022 : Affichage structuré
function showResult(data) {
    const output = {
        meta: {
            timestamp: new Date().toISOString(),
            status: "ISO_20022_COMPLIANT",
            message: "Transaction/Analyse traitée avec succès"
        },
        payload: data
    };
    outEl.textContent = JSON.stringify(output, null, 2);
}

// Gestion des exceptions conforme aux protocoles de sécurité
function showError(err) {
    const errorReport = {
        meta: {
            timestamp: new Date().toISOString(),
            status: "SECURITY_ALERT",
            code: "ERR_EXECUTION"
        },
        error: err.message || String(err)
    };
    outEl.textContent = JSON.stringify(errorReport, null, 2);
    console.error("[GloirePay Security Alert]:", err);
}

async function postJson(path, data) {
    const response = await fetch(path, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json' 
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error(`Échec conformité serveur : ${response.status}`);
    }
    return await response.json();
}

function parsePayload() {
    try {
        return JSON.parse(payloadEl.value.trim() || '{}');
    } catch (e) {
        return { error: "Format JSON invalide selon standard ISO 20022" };
    }
}

async function callEndpoint(path) {
    [btnA, btnAudit].forEach(btn => btn && (btn.disabled = true));
    
    try {
        const data = parsePayload();
        if (data.error) {
            outEl.textContent = data.error;
        } else {
            const result = await postJson(path, data);
            showResult(result);
        }
    } catch (e) {
        showError(e);
    } finally {
        [btnA, btnAudit].forEach(btn => btn && (btn.disabled = false));
    }
}

// Liaisons d'événements
if (btnA) btnA.addEventListener('click', () => callEndpoint('/analyze'));
if (btnAudit) btnAudit.addEventListener('click', () => callEndpoint('/audit'));
