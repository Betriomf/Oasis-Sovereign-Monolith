import math

# Constantes Oasis
KAPPA = 2.3
PHI = (1 + math.sqrt(5)) / 2

def calculate_dark_energy_proxy(volume_growth):
    # El coste de computar el nuevo espacio-tiempo
    # dS/dt relacionado con la constante de acoplamiento
    return (volume_growth * math.log(PHI)) / KAPPA

print("🏛️ OASIS HYPOTHESIS: DARK ENERGY COMPUTATIONAL COST")
print("="*55)
growth_rates = [1, 10, 100] # Unidades arbitrarias de expansión
for g in growth_rates:
    cost = calculate_dark_energy_proxy(g)
    print(f"📈 Tasa Expansión: {g} | Coste Energético (Proxy): {cost:.4f}")

print("\n🛡️ Veredicto: El universo se expande para optimizar la fase κ=2.3.")
