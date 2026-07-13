import time
import sys
import os

# On ajoute explicitement le dossier parent au PATH pour être sûr
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gloire_base import GloireBase
from src.blockchain_agent import GloireDevIA_Web3

# ... (le reste de ton code ne change pas)
