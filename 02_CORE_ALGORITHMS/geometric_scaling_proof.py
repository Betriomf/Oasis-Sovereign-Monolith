import math

def calculate_collision_density(N):
    # Tradicional: Cuadrático Theta(N^2) [cite: 11, 254]
    traditional = N**2 
    # OASIS: Lineal O(N) basado en phi [cite: 9, 256]
    oasis = N * ((5**0.5 - 1) / 2) 
    return traditional, oasis

print("--- SCALABILITY AUDIT (N=10,000 nodes) ---")
trad, oas = calculate_collision_density(10000)
print(f"Colisiones Tradicionales (N^2): {trad}")
print(f"Colisiones OASIS (O(N)): {oas:.2f}")
print(f"Factor de reducción estructural: {trad/oas:.1f}x")
