import time
import sys
import os

# Ajoute le dossier parent (racine) au chemin système une seule fois
# de manière propre pour que 'src' soit importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gloire_base import GloireBase
from src.blockchain_agent import GloireDevIA_Web3

class GloireOrchestrator:
    # ... (le reste de ta classe ne change pas)
