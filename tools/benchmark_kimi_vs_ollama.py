import time
import subprocess
import urllib.request
import json
import os

print("════════════════════════════════════════════════════════════════")
print("⚡ BENCHMARK INTEGRADO: MOTOR C99 PURO vs. OLLAMA LOCAL")
print("════════════════════════════════════════════════════════════════")

# 1. Benchmark Motor C99 Puro
c99_path = "./tools/oasis_c99_engine"
if os.path.exists(c99_path):
    t0 = time.perf_counter()
    res = subprocess.run([c99_path, "Pilar 378 Navier-Stokes"], capture_output=True, text=True)
    c99_latency_ms = (time.perf_counter() - t0) * 1000
    print(f"• Motor C99 (Zero-Framework) : Latencia total = {c99_latency_ms:.3f} ms")
    print(f"  Detalle tensores C99       : {res.stdout.strip()}")
else:
    print("• Motor C99                  : Binario no encontrado en tools/oasis_c99_engine")

# 2. Benchmark Ollama Local
ollama_url = "http://127.0.0.1:11434/api/generate"
prompt = "¿Cual es la capital de España? Responde en una sola palabra."
t0 = time.perf_counter()
try:
    req_data = json.dumps({"model": "aether:1.5b", "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(ollama_url, data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        ollama_total_s = (time.perf_counter() - t0)
        eval_count = data.get("eval_count", 0)
        eval_duration = data.get("eval_duration", 1) / 1e9
        tps = eval_count / eval_duration if eval_duration > 0 else 0
        print(f"\n• Ollama Local (aether:1.5b) : {eval_count} tokens generados en {ollama_total_s:.2f} s")
        print(f"  Velocidad de generación    : {tps:.2f} tokens/segundo")
        print(f"  Respuesta modelo           : {data.get('response', '').strip()}")
except Exception as e:
    print(f"\n• Ollama Local               : Fallo al consultar Ollama: {e}")

print("════════════════════════════════════════════════════════════════")
