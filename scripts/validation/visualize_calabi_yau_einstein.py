import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calabi_yau_map(z1, z2, k=5):
    """Proyección simplificada de una variedad de Calabi-Yau"""
    x = np.real(z1**k + z2**k)
    y = np.imag(z1**k - z2**k)
    z = np.real(z1 * z2)
    return x, y, z

def apply_einstein_curvature(X, Y, Z, data_mass_tb):
    """
    Aplica una deformación métrica basada en el Tensor de Riemann.
    Representa la 'Gravedad de los Datos': archivos masivos curvan el espacio-tiempo.
    """
    G_digital = 1.0e-2 # Constante gravitacional Oasis
    R = np.sqrt(X**2 + Y**2 + Z**2) + 0.1
    # Ecuación de campo: La masa curva la métrica
    curvature_depth = (G_digital * data_mass_tb) / R
    Z_curved = Z - curvature_depth * np.exp(-R)
    return X, Y, Z_curved

# --- 1. Generar malla irracional (Sucesión de Kronecker) ---
phi = (np.sqrt(5) + 1) / 2
t = np.linspace(0, 2*np.pi, 100)
u = np.linspace(0, np.pi, 100)
T, U = np.meshgrid(t, u)

Z1 = np.exp(1j * T) * np.sin(U)
Z2 = np.exp(1j * phi * T) * np.cos(U) # Rotación áurea

# --- 2. Comparativa de Campo ---
X, Y, Z_flat = calabi_yau_map(Z1, Z2)
# Simulamos un Data Center masivo (500 TB)
DATA_MASS_TB = 500
X, Y, Z_curved = apply_einstein_curvature(X, Y, Z_flat, DATA_MASS_TB)

# --- 3. Renderizado ---
fig = plt.figure(figsize=(14, 7), facecolor='black')
fig.suptitle("OASIS UNIFIED FIELD: Calabi-Yau + Einstein Curvature", color='white', fontsize=16)

# Subplot 1: Estado Base (Cuerdas)
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z_flat, cmap='cool', alpha=0.7, edgecolor='none')
ax1.set_axis_off()
ax1.set_title("Espacio Plano (Solo Cuerdas)", color='white')

# Subplot 2: Estado Curvado (Einstein)
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, Z_curved, cmap='magma', alpha=0.9, edgecolor='none')
ax2.set_axis_off()
ax2.set_title(f"Métrica de Riemann (Masa: {DATA_MASS_TB} TB)", color='#ffcc00')

print(f"✅ Hito alcanzado: La masa de {DATA_MASS_TB}TB ha curvado el espacio de metadatos.")
plt.show()
