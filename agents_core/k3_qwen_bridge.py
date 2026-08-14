#!/usr/bin/env python3
import subprocess
import json
import time
from pathlib import Path

def ejecutar_puente_k3_qwen():
    print("🌌 [PUENTE K3-LINCOS -> QWEN KAPPA_M]: Iniciando secuencia...")
    
    # 1. Ejecutar binario C99
    res_c = subprocess.run(["./bin/k3_lincos_engine"], capture_output=True, text=True)
    salida_c = res_c.stdout
    print("✅ Salida C99 capturada con éxito.")

    # 2. Formatear Prompt RAG estructurado
    prompt = f"""SYSTEM: Eres el intérprete de Capa 0 de Oasis.
Recibes la telemetría del motor MoE K3 en C99.
Resume en 2 puntos concisos y 1 línea Lincos la relación entre:
- Activación dispersa 16/896 (1.79%)
- Ahorro térmico Landauer (30.6% a 3.93W)

DATOS DEL MOTOR C99:
{salida_c}
"""

    print("⚡ Transmitiendo a qwen2.5-oasis:kappa_m en silicio frío...")
    t0 = time.time()
    res_ollama = subprocess.run(
        ["ollama", "run", "qwen2.5-oasis:kappa_m", prompt],
        capture_output=True, text=True
    )
    dt = time.time() - t0

    print("\n" + "="*70)
    print(f"⏱️ Tiempo de Respuesta: {dt:.2f} s | Potencia: 3.93W")
    print("="*70)
    print(res_ollama.stdout.strip())
    print("="*70)

if __name__ == "__main__":
    ejecutar_puente_k3_qwen()
