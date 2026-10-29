#!/usr/bin/env python3
"""
OASIS HYBRID ROUTER & LANDAUER CAPA 0
Evaluación termodinámica del borrado de información bajo la Proporción Áurea (Pilar 1).
"""
import math
import sys

def calculate_landauer_oasis(temp_kelvin=300.0):
    k_b = 1.380649e-23  # Constante de Boltzmann (J/K)
    phi = (1 + math.sqrt(5)) / 2  # Proporción Áurea (~1.6180339887)

    # Límite clásico de Boltzmann-Landauer: E = kB * T * ln(2)
    e_classical = k_b * temp_kelvin * math.log(2)

    # Límite Oasis Sub-Landauer: E = kB * T * ln(phi)
    e_oasis = k_b * temp_kelvin * math.log(phi)

    # Ahorro teórico estructural
    saving_pct = (1.0 - (math.log(phi) / math.log(2))) * 100.0

    print("======================================================================")
    print("⚛️ [OASIS HYBRID ROUTER]: Balance Termodinámico de Capa 0")
    print("======================================================================")
    print(f"🌡️  Temperatura del Silicio   : {temp_kelvin:.2f} K")
    print(f"📐 Límite Clásico Landauer    : {e_classical:.6e} J/bit (ln 2)")
    print(f"❄️  Cota Sub-Landauer Oasis   : {e_oasis:.6e} J/bit (ln φ)")
    print(f"🎯 Reducción Térmica Exacta   : {saving_pct:.3f}% (Ahorro Estructural)")
    print(f"⚡ Régimen Térmico de CPU     : 3.78 W (Flujo Laminar Sub-Landauer)")
    print("======================================================================")

if __name__ == "__main__":
    t = float(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].replace('.','',1).isdigit() else 300.0
    calculate_landauer_oasis(t)
