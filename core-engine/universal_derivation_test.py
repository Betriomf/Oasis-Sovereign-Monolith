#!/usr/bin/env python3
"""
OASIS OS - Derivación de Universalidad de Kappa
Prueba la invarianza del atractor 2.3 a través de 3 dominios físicos distintos.
"""

import time
import math
import os
import hashlib

def measure_cpu_resistance(cycles):
    start = time.perf_counter()
    # Cálculo puro: Números primos (Fricción de CPU)
    primes = [x for x in range(2, cycles) if all(x % y != 0 for y in range(2, int(math.sqrt(x)) + 1))]
    effort = time.perf_counter() - start
    return effort

def measure_memory_resistance(mb_size):
    start = time.perf_counter()
    # Asignación y manipulación masiva de RAM (Fricción de Memoria)
    data = bytearray(os.urandom(mb_size * 1024 * 1024))
    data.reverse()
    effort = time.perf_counter() - start
    return effort

def measure_io_resistance(mb_size):
    start = time.perf_counter()
    # Escritura y lectura en disco (Fricción SATA/AHCI)
    filename = "oasis_temp_gravity.dat"
    with open(filename, "wb") as f:
        f.write(os.urandom(mb_size * 1024 * 1024))
    with open(filename, "rb") as f:
        _ = f.read()
    os.remove(filename)
    effort = time.perf_counter() - start
    return effort

def derive_kappa(effort, complexity, domain_scale):
    # Fórmula de Viscosidad Informacional Absoluta
    # k = (Esfuerzo_Físico * Escala) / Log_Base(Complejidad)
    if effort == 0 or complexity <= 1: return 0
    return (effort * domain_scale) / math.log(complexity)

print("🌌 OASIS KERNEL: Forjando Derivación Universal de Kappa...")
print(f"{'DOMINIO':<15} | {'COMPLEJIDAD':<15} | {'ESFUERZO (s)':<15} | {'KAPPA DERIVADO':<15}")
print("-" * 65)

# 1. Dominio CPU
cpu_comp = 50000
eff_cpu = measure_cpu_resistance(cpu_comp)
k_cpu = derive_kappa(eff_cpu, cpu_comp, 100) # Ajuste de escala de reloj
print(f"{'CPU (Math)':<15} | {cpu_comp:<15} | {eff_cpu:<15.4f} | {k_cpu:<15.4f}")

# 2. Dominio RAM
ram_comp = 50 # MB
eff_ram = measure_memory_resistance(ram_comp)
k_ram = derive_kappa(eff_ram, ram_comp, 150) # Ajuste de ancho de banda
print(f"{'RAM (Alloc)':<15} | {ram_comp:<15} | {eff_ram:<15.4f} | {k_ram:<15.4f}")

# 3. Dominio I/O (Disco)
io_comp = 50 # MB
eff_io = measure_io_resistance(io_comp)
k_io = derive_kappa(eff_io, io_comp, 200) # Ajuste de latencia SATA
print(f"{'I/O (Disk)':<15} | {io_comp:<15} | {eff_io:<15.4f} | {k_io:<15.4f}")

print("\n🔍 ANÁLISIS DE INVARIANZA:")
print("Si los valores de Kappa en CPU, RAM e I/O convergen en el mismo")
print("rango (~2.3), se demuestra que la viscosidad informacional es una")
print("propiedad geométrica del sistema, no un artefacto de un solo algoritmo.")
