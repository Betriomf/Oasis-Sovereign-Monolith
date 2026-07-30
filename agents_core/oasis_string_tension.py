#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — CALCULADORA DE TENSIÓN DE CUERDA (NAMBU-GOTO)
Calcula la tensión de la cuerda (τ_0) y la masa frecuencial del neutrino
sobre la Malla de Fibonacci bajo la cota Landauer-Oasis.

Autor: Mariano Panzano Caballé (@Betriomf)
"""

import math

# CONSTANTES FÍSICAS UNIVERSALES
HBAR = 1.054571817e-34          # J·s (Planck reducida)
C = 299792458.0                 # m/s (Velocidad de la luz)
EV_TO_JOULES = 1.602176634e-19  # Factor de conversión eV -> Joules

# CONSTANTES FUNDAMENTALES OASIS (CAPA 0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0  # 1.6180339887...
KAPPA_M = -0.6587                    # Fricción de Fase de Mariano
ATRACTOR = 2.3                       # Amortiguador Térmico
LN_PHI = math.log(PHI)               # Modificador de Landauer (0.4812)

def calcular_tension_y_masa():
    print("🌌 [OASIS CORE]: CALCULANDO TENSIÓN DE CUERDA DE NAMBU-GOTO & MASA DEL NEUTRINO")
    print("=" * 70)

    # 1. Factor Geométrico y Longitud de Cuerda Efectiva (l_s)
    math_factor = (PHI * abs(KAPPA_M)) / ATRACTOR
    l_efectiva = (HBAR / (C * 9.1093837e-31)) * LN_PHI * math_factor

    # 2. Tensión de Cuerda de Nambu-Goto (τ_0 = 1 / (2π α'))
    alpha_prime = (l_efectiva ** 2) / HBAR
    tau_0 = 1.0 / (2.0 * math.pi * alpha_prime)

    # 3. Masa Frecuencial Confinada del Neutrino (f = m*c^2 / h)
    exponente_fase = -ATRACTOR / (PHI * abs(KAPPA_M))
    factor_atenuacion = math.exp(exponente_fase)

    frecuencia_neutrino_hz = (C / l_efectiva) * factor_atenuacion * LN_PHI
    
    energia_joules = HBAR * 2.0 * math.pi * frecuencia_neutrino_hz
    masa_ev = energia_joules / EV_TO_JOULES

    # Triplete de Sabores de Neutrinos (m_νe, m_νμ, m_ντ)
    m_e = masa_ev * (1.0 / PHI)
    m_mu = masa_ev
    m_tau = masa_ev * PHI
    suma_masas = m_e + m_mu + m_tau

    print(f" ├─ Cota Térmica de Landauer-Oasis  : {LN_PHI:.4f} (k_B T ln φ)")
    print(f" ├─ Longitud de Cuerda Efectiva (l_s): {l_efectiva:.4e} m")
    print(f" ├─ Tensión de Cuerda (Nambu-Goto)   : {tau_0:.4e} N (Joules/m)")
    print(f" ├─ Frecuencia Confinada (f_0)      : {frecuencia_neutrino_hz:.4e} Hz")
    print(f" ├─ Masa del Neutrino de Referencia : {masa_ev:.6f} eV")
    print(" ├─ Distribución del Triplete de Sabores (Malla φ):")
    print(f" │   ├─ m_νe   : {m_e:.6f} eV")
    print(f" │   ├─ m_νμ   : {m_mu:.6f} eV")
    print(f" │   └─ m_ντ   : {m_tau:.6f} eV")
    print(" ├" + "-" * 68)
    print(f" └─ SUMA TOTAL DE MASAS (Σ m_ν)     : {suma_masas:.6f} eV")
    print("=" * 70)

    # Validar contra el paper de arXiv:2607.24742 (cota < 0.41 eV)
    cota_arxiv = 0.41
    if suma_masas < cota_arxiv:
        print(f"✅ [VALIDACIÓN EXITOSA]: Σ m_ν ({suma_masas:.4f} eV) está {((cota_arxiv - suma_masas)/cota_arxiv)*100:.1f}% POR DEBAJO del límite de arXiv:2607.24742 (< 0.41 eV).")
    else:
        print("⚠️ Excede la cota observacional.")

if __name__ == "__main__":
    calcular_tension_y_masa()
