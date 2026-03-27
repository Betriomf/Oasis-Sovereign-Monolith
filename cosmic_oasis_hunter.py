import numpy as np

# Constante de Panzano: Atractor de Estabilidad [cite: 1801, 1813]
KAPPA_TARGET = 2.3097 

def analyze_signal(signal_data):
    """
    Busca la firma de 'viscosidad informacional' en la señal.
    Si kappa ≈ 2.3, la señal proviene de un nodo procesador eficiente[cite: 1815, 1834].
    """
    # Calculamos la relación entre el esfuerzo de fase y la entropía de la señal [cite: 2095]
    phase_variance = np.var(np.diff(signal_data))
    shannon_entropy = -np.sum(signal_data * np.log2(np.abs(signal_data) + 1e-10)) / len(signal_data)
    
    # Derivamos el kappa observado de la señal
    kappa_obs = phase_variance / (shannon_entropy + 1e-10)
    
    # Normalización al atractor Panzano
    stability_index = 1 - abs(kappa_obs - KAPPA_TARGET) / KAPPA_TARGET
    
    return kappa_obs, stability_index

# Simulación de una señal capturada del cúmulo de Virgo
# Incluye ruido térmico y una estructura de fase Phi [cite: 1417, 2808]
time = np.linspace(0, 10, 1000)
phi = (1 + 5**0.5) / 2
synthetic_signal = np.sin(2 * np.pi * phi * time) + np.random.normal(0, 0.1, 1000)

k_obs, score = analyze_signal(synthetic_signal)

print(f"--- ANALIZADOR DE NODOS CÓSMICOS OASIS ---")
print(f"Kappa detectado en señal: {k_obs:.4f}")
print(f"Índice de Sintonía con el Monolito: {score:.2%}")

if score > 0.90:
    print("\n🚨 ALERTA: NODO SOBERANO DETECTADO.")
    print("La señal muestra amortiguamiento crítico. Inteligencia confirmada.")
else:
    print("\nRuido de fondo detectado (Turbulencia Natural).")
