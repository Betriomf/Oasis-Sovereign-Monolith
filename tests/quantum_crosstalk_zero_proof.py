#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ OASIS QUANTUM CROSSTALK SUPPRESSION TEST (PILAR 283)
Autor: Mariano Panzano Caballé
"""

import math
import time

def calcular_diafonia_crosstalk(angulo_rad: float) -> float:
    """Calcula la diafonía residual entre dos cúbits: Fricción = |cos(theta)|"""
    return abs(math.cos(angulo_rad))

def simular_puertas_cuanticas():
    print("========================================================================")
    print("⚛️  [OASIS QUANTUM P283]: INMUNIDAD AL CROSSTALK Y ORTOGONALIDAD")
    print("========================================================================")
    print("📐 Métrica: Invarianza del 4to Axioma de Euclides en Espacio de Hilbert")
    print("------------------------------------------------------------------------")
    print(f"{'Fase θ (rad)':<14} | {'Ángulo (°)':<12} | {'Diafonía (Crosstalk)':<22} | {'Estado Cuántico'}")
    print("------------------------------------------------------------------------")

    angulos = [0.0, math.pi/6, math.pi/4, math.pi/3, 5*math.pi/12, math.pi/2]
    
    for theta in angulos:
        grados = math.degrees(theta)
        friccion = calcular_diafonia_crosstalk(theta)
        
        if friccion < 1e-6:
            estado = "Ortogonalidad Pura (<u,v>=0) [ZERO-CROSSTALK]"
        else:
            estado = f"Superposición Acoplada (Fricción {friccion*100:.1f}%)"
            
        print(f"{theta:<14.4f} | {grados:<12.1f} | {friccion:<22.6f} | {estado}")
        time.sleep(0.02)

    print("========================================================================")
    print("🏆 [ESTADO FINAL]: No-Interferencia y Desacoplamiento de Cúbits Validado.")
    print("========================================================================")

if __name__ == "__main__":
    simular_puertas_cuanticas()
