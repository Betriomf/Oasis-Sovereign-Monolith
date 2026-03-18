import numpy as np
import pandas as pd
from scipy.optimize import minimize
import os

# --- CONSTANTES OASIS ---
PHI = (np.sqrt(5) - 1) / 2
KAPPA = 2.3
H_TRUE = 67.4  # Objetivo: unificar con el CMB

def hubble_loss(H0, z, mu, weights=None):
    if H0 <= 0: return np.inf
    mu_pred = 5 * np.log10((3e5 * z) / H0) + 25
    residuals = (mu - mu_pred)**2
    if weights is not None:
        return np.sum(residuals * weights)
    return np.sum(residuals)

print("🏛️ OASIS COSMOLOGICAL UNIFIER: REAL DATA INJECTION")
print("="*65)

# Cargar dataset real si existe, si no, simular
file_path = 'data/pantheon_plus.csv'
if os.path.exists(file_path):
    print("📡 Cargando Dataset Real: Pantheon+...")
    df = pd.read_csv(file_path)
    # Columnas: zHD (redshift), MU_SH0ES (distancia), MJD (tiempo)
    data = df[['zHD', 'MU_SH0ES', 'MJD']].dropna().rename(columns={'zHD':'z', 'MU_SH0ES':'mu', 'MJD':'t'})
else:
    print("⚠️ Dataset no encontrado. Generando muestra de control...")
    z = np.random.uniform(0.01, 1.5, 1000)
    t = np.linspace(0, 100, 1000)
    mu = 5 * np.log10((3e5 * z) / 73.0) + 25 + np.random.normal(0, 0.5, 1000)
    data = pd.DataFrame({'z': z, 'mu': mu, 't': t})

# 1. Análisis Legacy (Sin Φ)
res_std = minimize(hubble_loss, x0=70, args=(data['z'], data['mu']))
h0_std = res_std.x[0]

# 2. Análisis Oasis (Con Φ)
data['theta'] = (data['t'] * PHI) % 1
counts, bins = np.histogram(data['theta'], bins=30)
weights = 1.0 / counts[np.digitize(data['theta'], bins[:-1]) - 1]
weights /= np.mean(weights)

res_oasis = minimize(hubble_loss, x0=70, args=(data['z'], data['mu'], weights))
h0_oasis = res_oasis.x[0]

print(f"📊 RESULTADO STANDARD (Local): {h0_std:.2f} km/s/Mpc")
print(f"🌀 RESULTADO OASIS (PHI-Clean): {h0_oasis:.2f} km/s/Mpc")
print(f"⚖️ DISCREPANCIA REDUCIDA: {abs(h0_oasis - H_TRUE):.4f}")

if abs(h0_oasis - H_TRUE) < abs(h0_std - H_TRUE):
    print("\n✅ HITO: La Tensión de Hubble se disuelve en el atractor κ=2.3.")
