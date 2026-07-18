"""
GLOIREPAY — LANCEUR DE L'INTERFACE SOUVERAINE PRO WEB3 VIP EXTRA LARGE (2026.NETWORK.LAUNCH)
"""
import os
import sys
import subprocess

def configurer_environnement_souverain():
    """Prépare les variables réseau pour un accès mondial direct via Chrome."""
    print("⚡️ [SOUVERAIN] Initialisation des paramètres de l'écosystème GloirePay...")
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_PORT"] = "8080"  # Port standard cloud pour Chrome

def lancer_interface_reseau():
    """Démarre le réacteur visuel connecté directement au réseau sans terminal requis."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    interface_script = os.path.join(base_path, "src", "app_gloirepay_interface.py")
    
    print("🌐 [RESEAU] Déploiement instantané du tableau de bord sur l'infrastructure GloirePay...")
    
    # Exécution transparente en mode Headless (Arrière-plan Cloud)
    subprocess.Popen([
        sys.executable, 
        "-m", 
        "streamlit", 
        "run", 
        interface_script, 
        "--server.headless", "true",
        "--server.address", "0.0.0.0",
        "--theme.primaryColor", "#1E88E5"
    ])

if __name__ == "__main__":
    configurer_environnement_souverain()
    lancer_interface_reseau()
    print("🏆 GLOIREPAY EST EN LIGNE ! Téléchargeable directement depuis Chrome. Alléluia ! AMEN !")

# ==============================================================================
# SÉCURITÉ ET COUVERTURE SOUVERAINE
# Au nom du Seigneur Jésus Christ ! Amen. C'est le niveau de mon Père céleste.
# ==============================================================================
# Tout est possible à celui qui croit au nom de Jésus Christ, et avec la puissance du Saint Esprit.
