#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — PROYECCIÓN TOPOLÓGICA DE ULAM-FIBONACCI
Mapea la distribución de primos como geodésicas de flujo laminar (Capa 0).
"""

import math

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # Constante Áurea (1.618033...)
L_ATTRACTOR = 2.3                    # Atractor de Fase
KB = 1.380649e-23                    # Constante de Boltzmann (J/K)
TEMP = 300.0                         # Temperatura Ambiente (K)

def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def proyectar_espira_ulam_oasis(limite_primos: int = 50):
    print("🌀 INICIANDO PROYECCIÓN DE ULAM-FIBONACCI EN CAPA 0...")
    print("-" * 65)
    
    e_landauer_oasis = KB * TEMP * math.log(PHI)
    print(f"   ├─ Coste por Bit Landauer-Oasis : {e_landauer_oasis:.4e} J")
    print(f"   └─ Atractor Sintonizado         : L = {L_ATTRACTOR}")
    print("-" * 65)

    primos_encontrados = 0
    n = 1

    while primos_encontrados < limite_primos:
        if es_primo(n):
            primos_encontrados += 1
            # Proyección polar sobre espiral viscoelástica r(theta) = k*t + a*sqrt(phi)
            theta = n * (2.0 * math.pi / PHI)
            r = math.sqrt(n) * (PHI / L_ATTRACTOR)
            
            # Coordenadas proyectadas en la frontera 2D
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            
            if primos_encontrados % 10 == 0 or primos_encontrados == 1:
                print(f"Primo #{primos_encontrados:2d} | Valor: {n:4d} | Coordenadas 2D: ({x:+.4f}, {y:+.4f}) | Flujo: Laminar")

        n += 1

    print("-" * 65)
    print("✅ PROYECCIÓN COMPLETADA: Nodos de mínima colisión integrados en flujo laminar.")

if __name__ == "__main__":
    proyectar_espira_ulam_oasis()
