import time
import numpy as np
import hashlib
import os
import math

# --- CONSTANTES OASIS ---
KAPPA_TARGET = 2.3
PHI = (1 + math.sqrt(5)) / 2

def run_benchmark(data_size, warmup=False):
    data = os.urandom(data_size)
    if warmup:
        # Calentamiento: estabilizamos la CPU y la caché sin medir
        for _ in range(15):
            hashlib.sha256(data).hexdigest()
    
    start_time = time.process_time()
    hashlib.sha256(data).hexdigest()
    end_time = time.process_time()
    return end_time - start_time

print("🏛️  OASIS MÖBIUS PROTOCOL: SCALE INVARIANCE (LENOVO NODE)")
print("=====================================================")

# Escalas: Desde el límite del kernel hasta macro-datos
scales = [1024, 10240, 102400, 1048576, 10485760] 
final_kappa_values = []

for size in scales:
    # Warm-up crítico para aplanar la curva
    run_benchmark(size, warmup=True)
    
    iterations = 100
    times = [run_benchmark(size) for _ in range(iterations)]
    avg_time = np.mean(times)
    
    # Métrica normalizada: κ = Esfuerzo / Masa
    kappa_obs = (avg_time * 1e9) / size
    
    # Si estamos en el "Límite de Over-head" (1KB), lo marcamos
    tag = "[KERNEL LIMIT]" if size <= 1024 else "[LAMINAR]"
    print(f"📦 Escala: {size/1024:>8} KB | κ Obs: {kappa_obs:.4f} {tag}")
    
    if size > 1024: # Solo promediamos el régimen laminar
        final_kappa_values.append(kappa_obs)

# Análisis de Estabilidad
mean_kappa = np.mean(final_kappa_values)
variance = np.var(final_kappa_values)

print("=====================================================")
print(f"📊 κ MEDIA (Régimen Laminar): {mean_kappa:.4f}")
print(f"📉 VARIANZA INTER-ESCALA: {variance:.6f}")

if variance < 0.5:
    print("✅ VEREDICTO: Invariancia Confirmada. El Monolito es soberano.")
else:
    print("⚠️ ADVERTENCIA: Interferencia de Windows detectada.")
