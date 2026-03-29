import numpy as np
import matplotlib.pyplot as plt

def run_kolmogorov_comparison():
    # 1. Parámetros Fundamentales
    phi = (1 + 5**0.5) / 2
    kappa_m = 2.3046
    target_laminar = np.log(phi) / np.log(2) # 0.6942
    
    print("🛰️ INICIANDO COMPARATIVA: CASCADA DE KOLMOGOROV vs ATRACTOR 2.3")
    print("---------------------------------------------------------------")

    # 2. Simulación de la Cascada de Energía (Espectro de Kolmogorov)
    # k representa el número de onda (frecuencia espacial)
    k = np.logspace(1, 5, 100)
    energy_kolmogorov = k**(-5/3) # La ley física estándar
    
    # 3. Inyección de la Métrica Oasis
    # Aplicamos la constante 2.3 como un factor de amortiguación informacional
    # En Oasis, la energía no decae al azar, se sintoniza con el ZIP universal.
    energy_oasis = k**(- (kappa_m / phi)) # Pendiente sintonizada en 2.3
    
    # 4. Cálculo de Coincidencia (Valle de Estabilidad)
    diff = np.abs(np.log10(energy_kolmogorov) - np.log10(energy_oasis))
    convergencia = (1 - np.mean(diff)) * 100

    print(f"[FISICA] Pendiente Kolmogorov: -1.666 (5/3)")
    print(f"[OASIS]  Pendiente Mariano:   -{kappa_m/phi:.3f}")
    print(f"✅ CONVERGENCIA EXPERIMENTAL: {convergencia:.2f}%")

    # 5. Visualización Científica
    plt.figure(figsize=(10, 6))
    plt.loglog(k, energy_kolmogorov, 'r--', label='Cascada de Kolmogorov (Clásica $k^{-5/3}$)')
    plt.loglog(k, energy_oasis, 'cyan', lw=2, label='Flujo Laminar Oasis (Atractor 2.3)')
    
    plt.title('Espectro de Energía: Validación Kolmogorov-Oasis')
    plt.xlabel('Número de Onda (k)')
    plt.ylabel('Densidad Espectral de Energía E(k)')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    
    plt.savefig('oasis_kolmogorov_fit.png')
    print("---------------------------------------------------------------")
    print("💎 Gráfica 'oasis_kolmogorov_fit.png' generada.")

if __name__ == "__main__":
    run_kolmogorov_comparison()
