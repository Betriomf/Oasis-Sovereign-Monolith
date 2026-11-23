#!/usr/bin/env python3
"""
OASIS SWARM — ESCANEO ESPECTRAL PRIMO-HOLOGRÁFICO (LÍNEA CRÍTICA vs LÍNEAS PARALELAS)
Evalúa la función de consenso / partición truncada sobre primos y compara mínimos de
resonancia en Re(s) = 0.5 frente a sigma in {0.3, 0.4, 0.6, 0.7}.
"""
import math
import cmath

def primes_up_to(n: int) -> list[int]:
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i : n+1 : i] = [False] * len(range(i*i, n+1, i))
    return [i for i, ok in enumerate(sieve) if ok]

PRIMES = primes_up_to(500)
LOG_PRIMES = [math.log(p) for p in PRIMES]

def zeta_approx_riemann_siegel_dirichlet(s: complex, terms: int = 400) -> complex:
    """Evaluación vía serie alternada de Dirichlet eta(s) / (1 - 2^(1-s)), válida para Re(s) > 0."""
    eta = 0j
    for n in range(1, terms + 1):
        sign = -1.0 if (n % 2 == 0) else 1.0
        eta += sign * cmath.exp(-s * math.log(n))
    denom = 1.0 - cmath.exp((1.0 - s) * math.log(2.0))
    return eta / denom if abs(denom) > 1e-12 else complex("inf")

def prime_phase_coherence(sigma: float, t: float) -> float:
    """Mide coherencia de fase de la red de primos p^(-sigma - i*t) bajo condición áurea."""
    acc = sum(cmath.exp(-complex(sigma, t) * lp) for lp in LOG_PRIMES)
    return abs(acc) / len(PRIMES)

KNOWN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178]

print("══════════════════════════════════════════════════════════════════════")
print("⚛️  [OASIS RIEMANN SPECTRAL SCAN — LÍNEA CRÍTICA 0.5 vs PARALELAS]")
print("──────────────────────────────────────────────────────────────────────")
print("  t (Im s)  | |zeta(0.5+it)| | |zeta(0.3+it)| | |zeta(0.7+it)| | Coherencia phi(0.5)")
print("------------+----------------+----------------+----------------+--------------------")
for t in KNOWN_ZEROS:
    z_half = abs(zeta_approx_riemann_siegel_dirichlet(complex(0.5, t)))
    z_03   = abs(zeta_approx_riemann_siegel_dirichlet(complex(0.3, t)))
    z_07   = abs(zeta_approx_riemann_siegel_dirichlet(complex(0.7, t)))
    coh    = prime_phase_coherence(0.5, t)
    print(f" {t:10.6f} |    {z_half:10.6f}  |    {z_03:10.6f}  |    {z_07:10.6f}  |     {coh:10.6f}")

print("\n📊 [BARRIDO DE MÍNIMOS LOCALES EN t ∈ [13.5, 38.5], paso 0.05]:")
for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
    minima = []
    t = 13.5
    vals = []
    while t <= 38.5:
        vals.append((t, abs(zeta_approx_riemann_siegel_dirichlet(complex(sigma, t)))))
        t = round(t + 0.05, 4)
    for i in range(1, len(vals) - 1):
        if vals[i][1] < vals[i-1][1] and vals[i][1] < vals[i+1][1] and vals[i][1] < 0.15:
            minima.append(f"t≈{vals[i][0]:.2f} (|ζ|={vals[i][1]:.4f})")
    print(f"  • sigma = {sigma:.1f} -> Mínimos profundos (<0.15): {len(minima)} | {', '.join(minima) if minima else 'Ninguno'}")
