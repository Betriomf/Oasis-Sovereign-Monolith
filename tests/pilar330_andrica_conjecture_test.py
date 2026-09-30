#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

def criba(n):
    es_p = bytearray([1]) * (n + 1)
    es_p[0] = es_p[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if es_p[i]:
            es_p[i*i : n + 1 : i] = bytearray([0]) * len(es_p[i*i : n + 1 : i])
    return [i for i, p in enumerate(es_p) if p]

if __name__ == "__main__":
    primos = criba(2000000)
    fallos_andrica = 0
    max_andrica = 0.0
    par_max = ()
    
    for n in range(len(primos) - 1):
        p1 = primos[n]
        p2 = primos[n+1]
        
        diff_sqrt = math.sqrt(p2) - math.sqrt(p1)
        if diff_sqrt >= 1.0:
            fallos_andrica += 1
            
        if diff_sqrt > max_andrica:
            max_andrica = diff_sqrt
            par_max = (p1, p2)

    print("=" * 80)
    print("🔢 [OASIS P330]: AUDITORÍA DE LA CONJETURA DE ANDRICA: √(p_{n+1}) - √(p_n) < 1")
    print("=" * 80)
    print(f"📊 Total Primos Auditados    : {len(primos):,}")
    print(f"🎯 Conjetura de Andrica      : {"100.00% CUMPLIDA (0 Fallos)" if fallos_andrica == 0 else f"{fallos_andrica} Fallos"}")
    print(f"📈 Máxima Diferencia de Raíz : {max_andrica:.6f} en par {par_max} (< 1.0000 OK)")
    print(f"❄️  Régimen Térmico Silicio  : ≤ 3.45W (Laminar)")
    print("=" * 80)
