import subprocess
import time

def run_hardware_probe(kappa_ns):
    # Inyectar valor al Kernel (si el sustrato lo permite) [cite: 382, 403]
    subprocess.run(f"sudo sysctl -w kernel.sched_migration_cost_ns={kappa_ns}", 
                   shell=True, capture_output=True)
    
    # Medición de rendimiento real (Instrucciones vs Fallos de Caché) [cite: 325, 510]
    cmd = "sudo perf stat -e instructions,cache-misses taskset -c 0 stress-ng --cpu 1 --timeout 10s"
    res = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    
    ins, misses = 0, 0
    for line in res.stderr.split('\n'):
        if "instructions" in line:
            parts = line.split()
            if parts: ins = int(parts[0].replace('.', '').replace(',', ''))
        if "cache-misses" in line:
            parts = line.split()
            if parts: misses = int(parts[0].replace('.', '').replace(',', ''))
    
    # Eficiencia: Trabajo útil por cada evento de fricción térmica [cite: 187, 219]
    return ins / (misses + 1)

print("\n--- 🔬 PRUEBA DE FALSIFICACIÓN CIEGA (OASIS) ---")
k_values = [500000, 1000000, 2300000, 5000000]
data = {}

for kv in k_values:
    print(f"Midiendo eficiencia para κ = {kv} ns...")
    data[kv] = run_hardware_probe(kv)

print("\n--- RESULTADOS REALES DEL SILICIO ---")
print(f"{'κ (ns)':<10} | {'Instrucciones/Fallo de Caché'}")
print("-" * 45)
for k, v in data.items():
    print(f"{k:<10} | {v:.2f}")

best_k = max(data, key=data.get)
print(f"\nAtractor empírico detectado en: {best_k} ns")
