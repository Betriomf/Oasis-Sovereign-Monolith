import time
import random
import math

def benchmark_stochastic(n=1000000):
    start = time.time()
    for _ in range(n):
        _ = random.random() # Simula PRNG de ~200 ciclos [cite: 269]
    return time.time() - start

def benchmark_phi_oasis(n=1000000):
    phi = (5**0.5 - 1) / 2
    offset = 0.5
    start = time.time()
    for k in range(n):
        _ = (offset + k * phi) % 1 # Aritmética O(1) de ~3 ciclos [cite: 127, 268]
    return time.time() - start

print("🚀 OASIS vs STOCHASTIC CPU BENCHMARK")
t_stoch = benchmark_stochastic()
t_oasis = benchmark_phi_oasis()
print(f"Stochastic: {t_stoch:.4f}s | OASIS: {t_oasis:.4f}s")
print(f"Mejora de Eficiencia: {((t_stoch/t_oasis)-1)*100:.1f}%")
