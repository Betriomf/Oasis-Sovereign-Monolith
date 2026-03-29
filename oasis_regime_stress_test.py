import subprocess
import time
import statistics
import re

def run_regime_test(kappa_val, label):
    kappa_ns = int(kappa_val * 1000000)
    # Intentamos inyectar la viscosidad en el Kernel
    subprocess.run(f"sudo sysctl -w kernel.sched_migration_cost_ns={kappa_ns}", 
                   shell=True, capture_output=True)
    
    print(f"\n--- RÉGIMEN {label} (κ = {kappa_val}) ---")
    measurements = []
    for i in range(10):
        cmd = "sudo perf stat -e instructions,cache-misses stress-ng --cpu 4 --timeout 3s 2>&1"
        out = subprocess.check_output(cmd, shell=True).decode()
        ins = int(re.search(r'([\d\.,]+)\s+instructions', out).group(1).replace('.', '').replace(',', ''))
        miss = int(re.search(r'([\d\.,]+)\s+cache-misses', out).group(1).replace('.', '').replace(',', ''))
        measurements.append(ins / (miss + 1))
    
    mean = statistics.mean(measurements)
    std = statistics.stdev(measurements)
    print(f"  Eficiencia Media: {mean:.2f} instr/miss")
    print(f"  Estabilidad (σ): {std:.2f}")
    return mean, std

# Ejecución de los 3 estados de la materia informacional
results = {}
results['Baja Viscosidad'] = run_regime_test(0.5, "SUB-CRÍTICO")
results['Oasis Target'] = run_regime_test(2.3, "CRÍTICO (PANZANO)")
results['Alta Viscosidad'] = run_regime_test(5.0, "SOBRE-CRÍTICO")
