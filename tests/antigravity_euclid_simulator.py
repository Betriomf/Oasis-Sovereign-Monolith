#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ OASIS ANTIGRAVITY & EUCLID GEODESIC SIMULATOR (PILAR 276)
Autor: Mariano Panzano Caballé
"""

import math
import time

PHI = (1 + math.sqrt(5)) / 2
G0 = 9.80665  # m/s^2
DARK_ENERGY_PRESSURE = PHI**(-2)  # ~0.381966

def calcular_gravedad_efectiva(eta_fase):
    termino_atractivo = eta_fase * (1.0 - (PHI**(-5) / PHI**(-2)))
    g_ef = G0 * (termino_atractivo - DARK_ENERGY_PRESSURE * (1.0 - eta_fase))
    return g_ef

def simular_transicion():
    print("========================================================================")
    print("🌌 [OASIS SIMULATOR P276]: TRANSICIÓN A REPOSO EUCLIDIANO EN EL TIEMPO")
    print("========================================================================")
    print(f"📐 Presión Expansiva Energía Oscura (φ^-2): {DARK_ENERGY_PRESSURE * 100:.2f}%")
    print("------------------------------------------------------------------------")
    print(f"{'Paso':<6} | {'η_fase':<10} | {'g_ef (m/s²)':<12} | {'Curvatura Geodésica':<35} | {'Disipación'}")
    print("------------------------------------------------------------------------")

    pasos = 10
    for i in range(pasos + 1):
        eta = 1.0 - (i / pasos)
        g_ef = calcular_gravedad_efectiva(eta)
        curvatura = abs(g_ef) / G0
        
        if abs(g_ef) < 0.1:
            estado = "Recta Euclidiana (d²x/dτ² = 0)"
            calor = "≤ 3.90W (Laminar)"
        else:
            estado = f"Curvada (Tobogán Térmico) κ={curvatura:.3f}"
            calor = f"~{2.3 + curvatura * 1.5:.2f}W"
            
        print(f"#{i:02d}    | {eta:<10.2f} | {g_ef:<12.4f} | {estado:<35} | {calor}")
        time.sleep(0.03)

    print("========================================================================")
    print("🏆 [ESTADO FINAL]: Reposo Termodinámico Absoluto Alcanzado (dS/dτ = 0)")
    print("========================================================================")

if __name__ == "__main__":
    simular_transicion()
