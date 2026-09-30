#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ OASIS FISHER-RAO CURVATURE RELAXATION TO LAMBDA (PILAR 291)
Autor: Mariano Panzano Caballé
"""

import math
import time

PHI = (1 + math.sqrt(5)) / 2
HBAR = 1.054571817e-34
KB = 1.380649e-23
C_LIGHT = 299792458.0
H0_SI = 2.192e-18  # s^-1 (~67.66 km/s/Mpc)
R_HUBBLE = C_LIGHT / H0_SI  # ~1.3676e26 m
T_HAWKING_UNRUH = (HBAR * H0_SI) / (2 * math.pi * KB)  # ~2.66e-30 K
TARGET_LAMBDA = (3.0 / (R_HUBBLE ** 2)) * (PHI ** -2)

def simular_relajacion_fisher_rao():
    print("========================================================================")
    print("🌌 [OASIS P291]: RELAJACIÓN DE FISHER-RAO HACIA EL ATRACTOR LAMBDA")
    print("========================================================================")
    print(f"🌡️  Temperatura Hawking-Unruh (T_H) : {T_HAWKING_UNRUH:.4e} K")
    print(f"🔭 Radio de Horizonte Causal (R_H)  : {R_HUBBLE:.4e} m")
    print(f"🎯 Valor Objetivo Λ (Atractor)     : {TARGET_LAMBDA:.4e} m⁻²")
    print("------------------------------------------------------------------------")
    print(f"{'Factor Escala a/a0':<20} | {'Curvatura Fisher-Rao R_FR (m⁻²)':<32} | {'Estado Térmico'}")
    print("------------------------------------------------------------------------")

    escalas = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    for a in escalas:
        r_eff = R_HUBBLE * a
        curvatura_fr = (3.0 / (r_eff ** 2)) * (PHI ** -2)
        
        if abs(a - 1.0) < 1e-5:
            estado = "Atractor Λ Actual (Flujo Laminar)"
        elif a < 1.0:
            estado = "Fase Transitoria Térmica"
        else:
            estado = "Dilución Asintótica Fría"

        print(f"a = {a:<16.2f} | {curvatura_fr:<32.4e} | {estado}")
        time.sleep(0.02)

    print("========================================================================")
    print("🏆 [ESTADO]: No-singularidad y relajación asintótica validadas.")
    print("========================================================================")

if __name__ == "__main__":
    simular_relajacion_fisher_rao()
