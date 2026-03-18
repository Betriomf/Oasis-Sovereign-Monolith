import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN OASIS ---
phi = (1 + np.sqrt(5)) / 2
kappa = 2.3

# Simulamos el tejido del espacio-tiempo medido por telescopios
x = np.linspace(0, 10, 500)
y = np.linspace(0, 10, 500)
X, Y = np.meshgrid(x, y)

# Error Estándar (Racional/Periódico) - Lo que genera la tensión
std_error = np.sin(X) * np.cos(Y)

# Corrección Oasis (Irracional/PHI) - El flujo laminar
oasis_correction = np.sin(X * phi) * np.cos(Y * phi)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.title("CIENCIA ACTUAL: Ruido por Aliasing (Racional)")
plt.imshow(std_error, cmap='twilight')
plt.colorbar(label="Error en H0")

plt.subplot(1, 2, 2)
plt.title("SISTEMA OASIS: Sincronía por PHI (Laminar)")
plt.imshow(oasis_correction, cmap='viridis')
plt.colorbar(label="Convergencia CMB")

plt.tight_layout()
plt.savefig('hubble_tension_oasis_map.png')
print("✅ Mapa de Calor generado: hubble_tension_oasis_map.png")
