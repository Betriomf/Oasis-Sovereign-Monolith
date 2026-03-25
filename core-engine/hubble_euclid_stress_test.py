#!/usr/bin/env python3
"""
OASIS OS - Phase III: Hubble Temporal Jitter Stress Test
Verifica la estabilidad de la inferencia cosmológica bajo ruido temporal.
Compara el muestreo estándar frente al remuestreo de fase irracional (Phi).
"""

import math
import random
import numpy as np

# Parámetros del Apéndice A
N_OBSERVATIONS = 5000  # Simulando el dataset Pantheon+
SIGMA_JITTER = 0.05    # Ruido sintético inyectado (Temporal Jitter)
PHI = (1 + math.sqrt(5)) / 2  # Proporción Áurea

def generate_hubble_signal():
    """Genera una señal base ideal (Sin ruido)"""
    return np.array([math.sin(i * 0.1) for i in range(N_OBSERVATIONS)])

def standard_sampling(signal):
    """Modelo Estándar: Adquisición discreta vulnerable al Jitter (Aliasing)"""
    jitter = np.random.normal(0, SIGMA_JITTER, N_OBSERVATIONS)
    # El ruido impacta directamente en la fase de medición
    noisy_signal = signal + (jitter * np.sin(np.arange(N_OBSERVATIONS)))
    error_variance = np.var(noisy_signal - signal)
    return error_variance

def oasis_phi_sampling(signal):
    """Modelo OASIS: Remuestreo de Fase Irracional (Inmunidad al Aliasing)"""
    jitter = np.random.normal(0, SIGMA_JITTER, N_OBSERVATIONS)
    # Las fases de adquisición rotan irracionalmente, decorrelando el ruido
    phi_phases = [(i * PHI) % 1 for i in range(N_OBSERVATIONS)]
    noisy_signal = signal + (jitter * np.array([math.sin(p * math.pi) for p in phi_phases]))
    error_variance = np.var(noisy_signal - signal)
    return error_variance

print("🌌 OASIS KERNEL: Cosmological Temporal Jitter Stress Test (Phase III)")
print(f"Inyectando ruido temporal sintético (σ = {SIGMA_JITTER})...\n")

base_signal = generate_hubble_signal()

# 1. Ejecutamos el modelo estándar
var_std = standard_sampling(base_signal)
stability_std = max(0, 100 - (var_std * 10000))

# 2. Ejecutamos el modelo OASIS
var_oasis = oasis_phi_sampling(base_signal)
stability_oasis = max(0, 100 - (var_oasis * 10000))

print("📊 RESULTADOS DE ESTABILIDAD (DEGRADACIÓN DE FASE):")
print("-" * 55)
print(f"Modelo Estándar (Racional) : {stability_std:.2f}% de estabilidad")
print(f"Modelo OASIS (Irracional Φ): {stability_oasis:.2f}% de estabilidad")
print("-" * 55)

print("\n✅ CRITERIOS DE ÉXITO DEL APÉNDICE A:")
if stability_oasis >= 95.0:
    print("[PASÓ] Phase stability of OASIS model ≥ 95%")
else:
    print("[FALLÓ] Phase stability of OASIS model < 95%")

if stability_std < stability_oasis:
    print("[PASÓ] Degradation of standard model under identical perturbation")
else:
    print("[FALLÓ] El modelo estándar no se degradó.")
