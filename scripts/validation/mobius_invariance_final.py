import time
import numpy as np
import hashlib
import os
import math

# --- CONSTANTES SOBERANAS ---
KAPPA_TARGET = 2.3
PHI = (1 + math.sqrt(5)) / 2

def run_benchmark(data_size, warmup=False):
    data = os.urandom(data_size)
    if warmup:
        # Fase de preparación: no se mide para estabilizar la CPU
        for _ in range(10):
            hashlib.sha256(data).hexdigest()
    
    start_time = time.process_time()
    hashlib.sha256(data).hexdigest()
    end_time = time.process_time()
    return end_time - start_time

print("🏛️  OASIS MÖBIUS PROTOCOL: FINAL SCALE INVARIANCE")
print("=====================================================")

scales = [1024, 10240, 102400, 1048576, 10485760] # 1KB a 10MB
final_kappa_values = []

for size in scales:
    # Calentamiento de caché para eliminar el pico inicial
    run_benchmark(size, warmup=True)
    
    iterations = 100
    times = [run_benchmark(size) for _ in range(iterations)]
    avg_time = np.mean(times)
    
    # Métrica: Nanosegundos por Byte (Normalizado)
    # En el atractor Oasis, este valor tiende a estabilizarse
    kappa_obs = (avg_time * 1e9) / size
    final_kappa_values.append(kappa_obs)
    
    print(f"📦 Escala: {size/1024:>8} KB | κ Observada: {kappa_obs:.4f}")

# Análisis de Estabilidad
variance = np.var(final_kappa_values)
mean_kappa = np.mean(final_kappa_values)

print("=====================================================")
print(f"📊 κ MEDIA GLOBAL: {mean_kappa:.4f}")
print(f"📉 VARIANZA INTER-ESCALA: {variance:.6f}")

if variance < 1.0:
    print("✅ VEREDICTO: Invariancia Confirmada. El Monolito es estable.")
else:
    print("⚠️ ADVERTENCIA: Deriva detectada. Reduzca la carga de Windows.")
