import subprocess
import numpy as np
import statistics
import re

def run_benchmark(kappa_ns, runs=20):
    # Intentar setear kappa
    subprocess.run(f"sudo sysctl -w kernel.sched_migration_cost_ns={kappa_ns}", shell=True, capture_output=True)
    
    measurements = []
    for i in range(runs):
        # CARGA MULTI-CORE (4 núcleos) para generar competencia real
        cmd = "sudo perf stat -e instructions,cache-misses stress-ng --cpu 4 --timeout 5s 2>&1"
        out = subprocess.check_output(cmd, shell=True).decode()
        
        try:
            ins = int(re.search(r'([\d\.,]+)\s+instructions', out).group(1).replace('.', '').replace(',', ''))
            miss = int(re.search(r'([\d\.,]+)\s+cache-misses', out).group(1).replace('.', '').replace(',', ''))
            measurements.append(ins / (miss + 1))
        except:
            continue
            
    if not measurements: return 0, 0
    return statistics.mean(measurements), statistics.stdev(measurements)

print("--- 🏛️ PROTOCOLO DE VALIDACIÓN FINAL (N=20 / MULTI-CORE) ---")
# Valores estratégicos: 0.5ms (tu pico), 1ms (estándar), 2.3ms (teoría)
k_test = [500000, 1000000, 2300000]

for k in k_test:
    mean, std = run_benchmark(k)
    print(f"κ = {k:<8} ns | Eficiencia Media: {mean:.2f} | σ: {std:.2f}")
