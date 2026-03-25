#!/usr/bin/env python3
import subprocess
import time
import math

def test_llm_gravity(tokens):
    # Inyectamos el concepto de los 2000s: --mlock (Memory Lock)
    # y desactivamos la interactividad para que solo calcule y salga.
    cmd = [
        "./llama.cpp/build/bin/llama-cli",
        "-m", "models/soberano_ligero.gguf",
        "-p", "OASIS",
        "-n", str(tokens),
        "--threads", "2",
        "-c", "128",
        "--mlock",           # <-- EL FIX DEL 2000: Bloquea el modelo en RAM
        "--no-display-prompt"
    ]
    
    start = time.perf_counter()
    # Ejecutamos capturando la salida para que no sature la terminal
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    effort = time.perf_counter() - start
    
    return effort

print("🌌 OASIS KERNEL: Test de Gravedad Neuronal (Optimizacion SIMD/mlock)")
print(f"{'TOKENS (Masa)':<15} | {'ESFUERZO (s)':<15} | {'KAPPA DERIVADO':<15}")
print("-" * 50)

# Masas adaptadas al sustrato de 4GB
token_masses = [4, 8, 16, 32]

for n in token_masses:
    effort = test_llm_gravity(n)
    
    # Derivación de la Constante (Ajuste de bus local)
    if n > 1:
        kappa = (effort * 1.5) / math.log(n)
    else:
        kappa = 0
        
    print(f"{n:<15} | {effort:<15.4f} | {kappa:<15.4f}")
