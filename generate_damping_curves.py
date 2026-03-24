import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 10, 500)

# Regímenes de Estabilidad (Sección 9.2)
underdamped = np.exp(-0.5 * t) * np.cos(3 * t)  # Jitter / Inestable
overdamped = np.exp(-0.2 * t)                  # Lento / Ineficiente
oasis_laminar = np.exp(-2.3 * t) * (1 + 2.3 * t) # Amortiguamiento Crítico (κ≈2.3)

plt.figure(figsize=(10, 6))
plt.plot(t, underdamped, label='Turbulent Regime (κ < 2)', color='red', linestyle='--')
plt.plot(t, overdamped, label='Overhead Dominated (κ > 3)', color='orange', linestyle=':')
plt.plot(t, oasis_laminar, label='OASIS Laminar Flow (κ ≈ 2.3)', color='cyan', linewidth=2.5)

plt.axhline(0, color='black', lw=1)
plt.title('Informational Stability: Transition to Critical Damping')
plt.xlabel('Computational Time (normalized)')
plt.ylabel('System State Deviation (x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('damping_stability_9_4.png')
print("✅ Visualización 'damping_stability_9_4.png' generada para la Sección 9.4")
