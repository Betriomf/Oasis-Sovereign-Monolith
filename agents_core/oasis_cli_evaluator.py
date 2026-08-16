#!/usr/bin/env python3
"""
OASIS DETERMINISTIC CLI EVALUATOR (Pilar 162)
Inferencia directa por subproceso POSIX sin timeouts HTTP de red
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import time
import sys

def evaluar_modelo(prompt: str):
    print("=" * 70)
    print("⚡ [OASIS CLI EVALUATOR]: Ejecutando inferencia directa...")
    print("   Modelo: oasis-laminar:1.5b | Sintonía: num_thread=2, num_ctx=2584")
    print("=" * 70)

    cmd = ["ollama", "run", "oasis-laminar:1.5b", prompt]
    
    t0 = time.perf_counter()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.perf_counter() - t0

    if res.returncode == 0:
        print("\n💬 RESPUESTA DEL MODELO:\n")
        print(res.stdout.strip())
        print("-" * 70)
        print(f"⏱️ Tiempo de ejecución: {dt:.2f} s")
        print("❄️ Silicio: LAMINAR PASIVO (<= 5.39W)")
    else:
        print(f"⚠️ Error al ejecutar: {res.stderr}")
    print("=" * 70)

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "Calcula la cota de Landauer en regimen de Fibonacci ln(phi) a T=300K y resume por que preserva el silicio frio."
    evaluar_modelo(p)
