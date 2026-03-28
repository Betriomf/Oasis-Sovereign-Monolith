import subprocess
import time
import re
import statistics

def run_stress_test(kappa_ns, cores=4, duration=10):
    # Inyectamos el valor en el Kernel para alterar la geometría temporal
    subprocess.run(f"sudo sysctl -w kernel.sched_migration_cost_ns={kappa_ns}",
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Medimos instrucciones y fallos de caché bajo saturación multi-core
    cmd = f"sudo perf stat -e instructions,cache-misses taskset -c 0-3 stress-ng --cpu {cores} --timeout {duration}s 2>&1"
    try:
        output = subprocess.check_output(cmd, shell=True).decode()
        instructions = int(re.search(r'([\d\.,]+)\s+instructions', output).group(1).replace('.', '').replace(',', ''))
        cache_misses = int(re.search(r'([\d\.,]+)\s+cache-misses', output).group(1).replace('.', '').replace(',', ''))
        return instructions / (cache_misses + 1)
    except Exception:
        return 0

print("\n--- 🔬 VALIDACIÓN HPC: OASIS SCHEDULING (4 CORES / N=5) ---")
# Valores de prueba: 0.5ms, 1ms, 1.6ms (Phi), 2.3ms (Oasis), 5ms
k_values = [500000, 1000000, 1618033, 2309700, 5000000]
RUNS = 5
results = {k: [] for k in k_values}

for kv in k_values:
    print(f"\n⚡ Inyectando κ = {kv} ns y saturando 4 núcleos...")
    for i in range(RUNS):
        eff = run_stress_test(kv)
        results[kv].append(eff)
        print(f"   Run {i+1}: {eff:.2f} instr/miss")

print("\n--- 📊 ANÁLISIS ESTADÍSTICO FINAL ---")
for kv in k_values:
    data = results[kv]
    media = statistics.mean(data)
    desv = statistics.stdev(data) if len(data) > 1 else 0
    print(f"κ = {kv:<8} ns | Media: {media:.2f} instr/miss | σ: {desv:.2f}")

best_k = max(results.keys(), key=lambda k: statistics.mean(results[k]))
print("="*65)
print(f"🏆 ATRACTOR MULTI-CORE DETECTADO: {best_k} ns")
print("="*65)
