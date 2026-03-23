import numpy as np

# Constantes Soberanas
KAPPA = 2.3
PHI = (1 + np.sqrt(5)) / 2

def laminar_smoothing(t):
    """Aplica suavização trigonométrica baseada em PHI para evitar jitter."""
    return np.sin(t * PHI) * np.exp(-t / KAPPA)

def calculate_informational_gravity(effort, complexity):
    """Calcula a κ local e verifica se estamos no regime laminar."""
    kappa_obs = effort / complexity
    status = "LAMINAR" if kappa_obs < KAPPA else "VISCOSO"
    return kappa_obs, status
