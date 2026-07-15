import pytest
import asyncio
from src.blockchain_agent import GloireDevIA_Web3

# Fixture persistante pour éviter les reconnexions multiples (Gain de performance)
@pytest.fixture(scope="module")
def agent():
    return GloireDevIA_Web3()

@pytest.mark.asyncio
async def test_souverainete_connexion(agent):
    """Vérification immédiate de la connectivité au nœud zkEVM."""
    assert agent.w3.is_connected(), "ALERTE : Nœud zkEVM inaccessible"
    chain_id = agent.w3.eth.chain_id
    assert chain_id == 1101, f"ALERTE : Mauvais réseau détecté (ChainID: {chain_id})"

@pytest.mark.asyncio
async def test_audit_tresorerie_vip(agent):
    """Audit rapide et sécurisé de la trésorerie souveraine."""
    # Simulation de l'appel pour valider la réponse du contrat
    status = agent.get_treasury_status()
    
    # Vérification des conditions critiques
    assert status is not None, "ERREUR : Réponse trésorerie nulle"
    assert status.get("status") == "online", "ALERTE : Trésorerie hors ligne"
    
    # Validation du solde (doit être positif pour le déploiement)
    balance = float(status.get("balance_wei", 0))
    assert balance > 0, "ALERTE : Solde insuffisant pour déploiement souverain"

@pytest.mark.asyncio
async def test_latence_rpc(agent):
    """Mesure de performance : latence minimale requise."""
    start_time = asyncio.get_event_loop().time()
    block = agent.w3.eth.get_block('latest')
    end_time = asyncio.get_event_loop().time()
    
    latency = end_time - start_time
    assert latency < 2.0, f"ALERTE : Latence réseau trop élevée ({latency:.2f}s)"
    assert block is not None, "ERREUR : Impossible de récupérer le dernier bloc"
