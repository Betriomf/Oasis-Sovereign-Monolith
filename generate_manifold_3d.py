import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definimos el espacio de fase (Tiempo vs Complejidad)
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)

# Modelo de Potencial Informacional (Sección 7.3)
# Representa la "curvatura" inducida por la latencia y colisiones
phi_turbulent = np.sin(10 * np.pi * X) * np.cos(10 * np.pi * Y) * 0.5
phi_laminar = (X**2 + Y**2) * 0.1 # Superficie suave tipo geodésica

fig = plt.figure(figsize=(12, 6))

# Subplot 1: Régimen Racional (Turbulento)
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, phi_turbulent, cmap='magma', alpha=0.8)
ax1.set_title('Rational Landscape (Entropy Peaks)')
ax1.set_zlabel('Potential Φ_info')

# Subplot 2: Régimen OASIS (Laminar/Geodésico)
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, phi_laminar, cmap='viridis', alpha=0.8)
ax2.set_title('OASIS Manifold (κ ≈ 2.3 Geodesic)')
ax2.set_zlabel('Potential Φ_info')

plt.tight_layout()
plt.savefig('informational_manifold_7_3.png')
print("✅ Visualización 'informational_manifold_7_3.png' generada para la Sección 7.3")
