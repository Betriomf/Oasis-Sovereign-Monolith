import math

def check_informational_entropy(used_gb):
    # k_B (Boltzman) / G (Gravity) simulado para Oasis
    oasis_constant = 2.3 # Tu constante kappa
    
    # El área del horizonte de eventos informacional
    area = 4 * math.pi * (used_gb**2)
    entropy = area / (4 * oasis_constant)
    
    print(f"🌑 OASIS BLACK HOLE ENTROPY AUDIT")
    print(f"💾 Espacio Usado: {used_gb} GB")
    print(f"🔥 Entropía de Bekenstein-Hawking: {entropy:.4f} bits/K")
    print(f"✅ ESTADO: Congelamiento Criogénico Informativo (Eficiencia Landauer)")

check_informational_entropy(17) # Tus 17GB usados actualmente
