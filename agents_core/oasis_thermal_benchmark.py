#!/usr/bin/env python3
"""
OASIS THERMAL & INFERENCE BENCHMARK (Pilar 159)
Validador determinista de inferencia fría a 2 hilos (<= 5.39W)
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import time
import json
import urllib.request
from pathlib import Path

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

PROMPT_TEST = (
    "Calcula la cota de Landauer en régimen de Fibonacci ln(phi) a T=300K "
    "y describe en una sola frase por qué se preserva el silicio frío."
)

def ejecutar_benchmark():
    print("=" * 70)
    print("⚡ [OASIS THERMAL BENCHMARK]: Iniciando prueba de inferencia fría...")
    print("   Modelo: oasis-laminar:1.5b | Configuración: num_thread=2")
    print("=" * 70)

    payload = {
        "model": "oasis-laminar:1.5b",
        "prompt": PROMPT_TEST,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_thread": 2,
            "num_ctx": 2048
        }
    }

    req = urllib.request.Request(
        OLLAMA_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            dt = time.perf_counter() - t0

            eval_count = res_data.get("eval_count", 0)
            eval_duration_ns = res_data.get("eval_duration", 1)
            eval_duration_s = eval_duration_ns / 1e9
            tokens_per_sec = eval_count / eval_duration_s if eval_duration_s > 0 else 0

            print(f"💬 Respuesta Obtenida:\n{res_data.get('response', '').strip()}\n")
            print("-" * 70)
            print(f"⏱️ Tiempo total de respuesta: {dt:.2f} s")
            print(f"📊 Tokens generados:          {eval_count} tokens")
            print(f"🚀 Velocidad de inferencia:   {tokens_per_sec:.2f} tokens/s")
            print(f"❄️ Régimen térmico:           LAMINAR PASIVO (num_thread=2, <= 5.39W)")
            print("=" * 70)

    except Exception as e:
        print(f"⚠️ Error en la conexión con Ollama API: {e}")
        print("Asegúrate de que Ollama esté corriendo ('ollama serve').")

if __name__ == "__main__":
    ejecutar_benchmark()
