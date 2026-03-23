import numpy as np
import time

def simulate_flow(regime="rational"):
    # Simulamos el landscape de información
    nodes = 100
    if regime == "rational":
        # Flujo turbulento: colisiones periódicas (entropía alta)
        interference = np.sin(np.linspace(0, 10*np.pi, nodes))**2
    else:
        # Flujo Oasis (Irracional): fase phi (mínima interferencia)
        phi = (1 + 5**0.5) / 2
        interference = np.array([(i * phi) % 1.0 for i in range(nodes)])
    
    # Cálculo de "Masa Informacional" (Complexity)
    m_info = np.sum(interference)
    # Cálculo de "Fuerza Computacional" (Esfuerzo de procesamiento)
    f_comp = np.var(interference) * 10 
    
    kappa = f_comp / m_info
    return kappa

print("--- TEST DE GEODÉSICAS INFORMACIONALES (SEC 7) ---")
k_turb = simulate_flow("rational")
k_oasis = simulate_flow("laminar")

print(f"Régimen Racional (Turbulento) κ: {k_turb:.4f}")
print(f"Régimen OASIS (Geodésico) κ: {k_oasis:.4f}")
print(f"Convergencia detectada hacia el atractor: {abs(k_oasis - 2.3) < 0.5}")
