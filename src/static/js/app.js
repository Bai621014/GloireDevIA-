// src/static/js/app.js
// Minimal UI client amélioré : envoie JSON à /analyze ou /audit et affiche la réponse,
// affiche les erreurs explicitement dans le bloc résultat.

const $ = sel => document.querySelector(sel);
const payloadEl = $('#payload');
const outEl = $('#output');
const btnA = $('#btnAnalyze');
const btnAudit = $('#btnAudit');

function showResult(obj) {
  outEl.textContent = JSON.stringify(obj, null, 2);
}

function showError(err) {
  // err peut être une Error ou un objet {status, text} renvoyé par le serveur
  if (!err) {
    outEl.textContent = 'Erreur : requête échouée (erreur inconnue)';
    return;
  }
  if (err instanceof Error) {
    outEl.textContent = 'Erreur : ' + (err.message || String(err));
    console.error(err);
    return;
  }
  if (typeof err === 'object' && err.status) {
    outEl.textContent = `Erreur ${err.status} : ${err.text || JSON.stringify(err)}`;
    console.error('HTTP erreur :', err);
    return;
  }
  outEl.textContent = 'Erreur : ' + String(err);
  console.error(err);
}

async function postJson(path, data) {
  try {
    const res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data),
    });

    const ct = res.headers.get('content-type') || '';

    // Traiter les codes HTTP non-OK
    if (!res.ok) {
      // essayer de lire le corps (json ou texte) pour donner un message utile
      try {
        if (ct.includes('application/json')) {
          const payload = await res.json();
          return { error: true, status: res.status, payload };
        } else {
          const text = await res.text();
          return { error: true, status: res.status, text };
        }
      } catch (e) {
        return { error: true, status: res.status, text: `Impossible de lire la réponse (content-type=${ct})` };
      }
    }

    // OK : parse JSON si possible, sinon renvoyer texte
    if (ct.includes('application/json')) {
      return await res.json();
    } else {
      return { status: res.status, text: await res.text() };
    }
  } catch (e) {
    // Erreur réseau / CORS / autre (fetch rejette)
    throw e;
  }
}

function parsePayload() {
  const raw = (payloadEl && payloadEl.value || '').trim();
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch (e) {
    // Ne pas échouer silencieusement : retourner l'input brut sous clef 'raw'
    return { raw };
  }
}

async function callEndpoint(path) {
  // UI lock
  if (btnA) btnA.disabled = true;
  if (btnAudit) btnAudit.disabled = true;
  try {
    const data = parsePayload();
    const result = await postJson(path, data);

    // Si postJson a renvoyé l'objet d'erreur formatté
    if (result && result.error) {
      if (result.payload) {
        showError({ status: result.status, text: JSON.stringify(result.payload) });
      } else {
        showError({ status: result.status, text: result.text || 'Erreur serveur' });
      }
      return;
    }

    showResult(result);
  } catch (e) {
    // Affichage explicite de l'erreur (conformément à votre demande)
    showError(e);
  } finally {
    // unlock UI
    if (btnA) btnA.disabled = false;
    if (btnAudit) btnAudit.disabled = false;
  }
}

if (btnA) btnA.addEventListener('click', async () => callEndpoint('/analyze'));
if (btnAudit) btnAudit.addEventListener('click', async () => callEndpoint('/audit'));
