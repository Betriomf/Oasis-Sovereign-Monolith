import subprocess
import numpy as np

def test_k(k_val):
    k_ns = int(k_val * 1000000)
    subprocess.run(f"sudo sysctl -w kernel.sched_migration_cost_ns={k_ns}", shell=True, capture_output=True)
    cmd = "sudo perf stat -e instructions,cache-misses taskset -c 0 stress-ng --cpu 1 --timeout 5s 2>&1"
    out = subprocess.check_output(cmd, shell=True).decode()
    ins = int(re.search(r'([\d\.,]+)\s+instructions', out).group(1).replace('.', '').replace(',', ''))
    miss = int(re.search(r'([\d\.,]+)\s+cache-misses', out).group(1).replace('.', '').replace(',', ''))
    return ins / (miss + 1)

import re
print("🔍 ESCANEANDO TODA LA BANDA DE κ...")
results = {}
# Probamos desde 0.1 hasta 3.0 en pasos finos
for k in np.arange(0.1, 3.1, 0.2):
    eff = test_k(k)
    print(f"κ = {k:.1f} ms | Eficiencia: {eff:.2f}")
    results[k] = eff

print(f"🏆 MEJOR VALOR PARA TU SILICIO: {max(results, key=results.get)} ms")
