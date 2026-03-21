import time
import hashlib
import os

def measure_kappa(size_kb):
    data = os.urandom(size_kb * 1024)
    start = time.process_time()
    hashlib.sha256(data).hexdigest()
    end = time.process_time()
    # Esfuerzo normalizado
    effort = (end - start) * 1e6
    kappa = effort / size_kb
    return kappa

print("🏛️ OASIS TRUTH TEST: SCALE INVARIANCE")
for size in [100, 1000, 10000]:
    k = measure_kappa(size)
    print(f"📦 Escala: {size}KB | κ Observada: {k:.4f}")
