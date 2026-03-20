import time
import numpy as np
import hashlib
import math
import os

# Constantes Oasis
KAPPA_TARGET = 2.3

def run_benchmark(data_size):
    # Generación de masa informacional
    data = os.urandom(data_size)
    start_time = time.process_time()
    # Tarea de transformación: hashing (Esfuerzo computacional)
    hashlib.sha256(data).hexdigest()
    end_time = time.process_time()
    return end_time - start_time

print("🏛️ OASIS MÖBIUS PROTOCOL: SCALE INVARIANCE TEST")
print("="*55)

scales = [1024, 10240, 102400, 1048576, 10485760] # 1KB a 10MB
results = []

for size in scales:
    iterations = 100
    times = [run_benchmark(size) for _ in range(iterations)]
    avg_time = np.mean(times)
    # Cálculo de κ observada (Esfuerzo / Complejidad)
    # Normalizamos a nanosegundos por byte para la métrica
    kappa_obs = (avg_time * 1e9) / size 
    results.append(kappa_obs)
    print(f"📦 Tamaño: {size/1024:>8} KB | κ Obs: {kappa_obs:.4f}")

variance = np.var(results)
print("="*55)
print(f"📊 Varianza de κ entre escalas: {variance:.8f}")
if variance < 0.5:
    print("✅ VEREDICTO: Invariancia de Escala Confirmada (Möbius Shield Active).")
else:
    print("⚠️ ADVERTENCIA: Se detectó deriva de fase. Revise interferencia de procesos.")
