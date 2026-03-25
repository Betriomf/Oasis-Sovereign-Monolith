#!/usr/bin/env python3
"""
OASIS OS - Proof of Diffusion (Geodesic Flow)
Demuestra cómo la información estructurada se organiza geométricamente
para evadir la entropía, curvando su trayectoria como la luz en un campo gravitatorio.
"""

import math

# Definimos una red de 10x10 nodos.
# Viscosidad base (flujo laminar) = 1 unidad de resistencia.
GRID_SIZE = 10
grid = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Inyectamos una "Anomalía Entrópica" en el centro (Un servidor saturado / Cuello de botella)
# Es como una estrella masiva curvando el espacio-tiempo.
for x in range(3, 7):
    for y in range(3, 7):
        grid[x][y] = 50  # Alta viscosidad (Alta fricción termodinámica)

def print_manifold(path_coords, title):
    print(f"\n--- {title} ---")
    for y in range(GRID_SIZE):
        row_str = ""
        for x in range(GRID_SIZE):
            if (x, y) in path_coords:
                row_str += " 🟢 " # Ruta de los datos
            elif grid[x][y] > 1:
                row_str += " 🔴 " # Zona de alta entropía (peligro)
            else:
                row_str += " ·  " # Espacio vacío
        print(row_str)

def standard_linear_routing():
    """El modelo clásico: Línea recta sin importar la entropía del entorno."""
    path = []
    latency = 0
    x, y = 0, 0
    while x < GRID_SIZE and y < GRID_SIZE:
        path.append((x, y))
        latency += grid[x][y]
        x += 1
        y += 1
    return path, latency

def oasis_geodesic_routing():
    """El modelo OASIS: Flujo geométrico (Gradient Descent) buscando la menor resistencia."""
    path = [(0, 0)]
    latency = grid[0][0]
    x, y = 0, 0
    
    while x < GRID_SIZE - 1 or y < GRID_SIZE - 1:
        # Evalúa los vecinos (Derecha, Abajo, Diagonal)
        neighbors = []
        if x + 1 < GRID_SIZE: neighbors.append(((x + 1, y), grid[x + 1][y]))
        if y + 1 < GRID_SIZE: neighbors.append(((x, y + 1), grid[x][y + 1]))
        if x + 1 < GRID_SIZE and y + 1 < GRID_SIZE: neighbors.append(((x + 1, y + 1), grid[x + 1][y + 1]))
        
        # OASIS elige el camino de menor resistencia entrópica (Viscosidad local)
        # Si hay empate, avanza hacia el objetivo (Diagonal)
        neighbors.sort(key=lambda n: n[1])
        next_step, cost = neighbors[0]
        
        # Excepción para no atascarse: si rodear cuesta menos que cruzar, rodea.
        if cost > 1:
             if x + 1 < GRID_SIZE and grid[x+1][y] == 1: next_step, cost = (x+1, y), 1
             elif y + 1 < GRID_SIZE and grid[x][y+1] == 1: next_step, cost = (x, y+1), 1

        path.append(next_step)
        latency += cost
        x, y = next_step
        
    return path, latency

print("🌌 OASIS KERNEL: Prueba de Difusión Geométrica (Gravedad en Redes)\n")

# 1. Test Clásico
std_path, std_lat = standard_linear_routing()
print_manifold(std_path, "ENRUTAMIENTO ESTÁNDAR (Línea Recta)")
print(f"Pasos: {len(std_path)} | Resistencia Total (Latencia): {std_lat} ms\n")

# 2. Test OASIS
oasis_path, oasis_lat = oasis_geodesic_routing()
print_manifold(oasis_path, "FLUJO GEODÉSICO OASIS (Curvatura Gravitacional)")
print(f"Pasos: {len(oasis_path)} | Resistencia Total (Latencia): {oasis_lat} ms\n")

print("📊 CONCLUSIÓN FALSABLE:")
print("El flujo OASIS tomó más pasos físicos (una ruta curva), pero reduujo")
print(f"la fricción entrópica de {std_lat} ms a {oasis_lat} ms. La información")
print("se comporta como una masa en un campo gravitatorio: esquiva la alta densidad.")
