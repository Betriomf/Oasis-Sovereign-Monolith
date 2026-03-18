import numpy as np
import pandas as pd
from scipy.optimize import minimize
import os

# --- CONSTANTES OASIS (Sintonización Zenodo) ---
PHI = (np.sqrt(5) - 1) / 2
KAPPA = 2.3
H_TRUE = 67.4  # Valor de consenso CMB

def hubble_loss(H0, z, mu, weights=None):
    if H0 <= 0: return np.inf
    mu_pred = 5 * np.log10((3e5 * z) / H0) + 25
    residuals = (mu - mu_pred)**2
    return np.sum(residuals * weights) if weights is not None else np.sum(residuals)

print("🏛️ OASIS HUBBLE UNIFIER: ZENODO COMPLIANCE MODE")
print("="*65)

file_path = 'data/pantheon_plus.csv'
data_loaded = False

if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
    try:
        df = pd.read_csv(file_path)
        # Mapeo flexible para columnas de Zenodo/Pantheon+
        col_map = {
            'zHD': 'z', 'zhel': 'z',
            'MU_SH0ES': 'mu', 'mu': 'mu',
            'MJD': 't', 'time': 't'
        }
        # Intentamos encontrar las columnas correctas
        available = [c for c in df.columns if c in col_map]
        if len(available) >= 3:
            data = df[available].rename(columns=col_map)
            data = data.dropna().head(1500) # Tomamos una muestra representativa
            print(f"✅ Dataset Zenodo detectado. Registros: {len(data)}")
            data_loaded = True
    except Exception as e:
        print(f"⚠️ Error al procesar CSV: {e}")

if not data_loaded:
    print("📡 Generando Muestra Sintética basada en Zenodo 18271610...")
    # Creamos datos que imitan la Tensión de Hubble (73 local vs 67 global)
    z = np.random.uniform(0.01, 1.5, 1200)
    t = np.linspace(50000, 60000, 1200) # Escala MJD real
    # Generamos con sesgo de resonancia (Aliasing)
    mu = 5 * np.log10((3e5 * z) / 73.2) + 25 + np.random.normal(0, 0.4, 1200)
    data = pd.DataFrame({'z': z, 'mu': mu, 't': t})

# 1. Análisis Legacy
res_std = minimize(hubble_loss, x0=70, args=(data['z'], data['mu']))
h0_std = res_std.x[0]

# 2. Análisis Oasis (Eliminación de Aliasing por PHI)
data['theta'] = (data['t'] * PHI) % 1
counts, bins = np.histogram(data['theta'], bins=40)
weights = 1.0 / counts[np.digitize(data['theta'], bins[:-1]) - 1]
weights /= np.mean(weights)

res_oasis = minimize(hubble_loss, x0=70, args=(data['z'], data['mu'], weights))
h0_oasis = res_oasis.x[0]

print(f"\n📊 RESULTADO STANDARD (Local Bias):  {h0_std:.2f} km/s/Mpc")
print(f"🌀 RESULTADO OASIS (Phase-Unlocked): {h0_oasis:.2f} km/s/Mpc")
print(f"🛡️  FACTOR DE CORRECCIÓN:            {abs(h0_std - h0_oasis):.4f}")

if abs(h0_oasis - H_TRUE) < abs(h0_std - H_TRUE):
    print("\n✅ CONCLUSIÓN: El remuestreo irracional reduce la tensión.")
    print("🚀 El Monolito valida la convergencia hacia el valor del CMB.")
