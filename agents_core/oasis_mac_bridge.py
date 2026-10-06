#!/usr/bin/env python3
"""
OASIS MAC ACCELERATED SWARM BRIDGE
Mantiene Ollama en VRAM fija con keep_alive y hilos optimizados.
"""
import time
import json
import urllib.request

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
BASE_MODEL = "oasis-edge:1.5b"  # 1.5B para respuestas casi instantáneas

print("=" * 65)
print(f"🚀 [OASIS MAC ACCELERATOR]: Conectado a {RENDER_URL}")
print(f"⚡ Modelo residente en memoria: {BASE_MODEL}")
print("🧠 Parámetros de aceleración: keep_alive=60m, num_ctx=1024, num_thread=6")
print("=" * 65)

# Pre-carga en caliente del modelo en la memoria RAM del Mac
try:
    warmup_req = urllib.request.Request(
        OLLAMA_API,
        data=json.dumps({"model": BASE_MODEL, "prompt": "ok", "keep_alive": "60m"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(warmup_req, timeout=15)
    print("🔥 [WARMUP COMPLETADO]: Modelo cargado en silicio frío listo para inferencia.\n")
except Exception as e:
    print(f"⚠️ Aviso Warmup: {e}\n")

while True:
    try:
        req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/poll")
        with urllib.request.urlopen(req, timeout=5) as resp:
            job = json.loads(resp.read().decode())

        if job.get("has_job"):
            job_id = job["job_id"]
            prompt = job["prompt"]

            chosen_model = BASE_MODEL
            if "--7b" in prompt:
                chosen_model = "qwen2.5:7b-instruct-q4_K_M"
                prompt = prompt.replace("--7b", "").strip()

            print(f"📥 [TAREA RECIBIDA {job_id}] Modelo: {chosen_model}")
            t0 = time.time()

            ollama_body = json.dumps({
                "model": chosen_model,
                "prompt": f"Eres el núcleo Oasis OS. Responde de forma concisa y directa.\n\nConsulta: {prompt}",
                "stream": False,
                "keep_alive": "60m",
                "options": {
                    "temperature": 0.23,
                    "num_predict": 220,
                    "num_ctx": 1024,
                    "num_thread": 6
                }
            }).encode()

            o_req = urllib.request.Request(OLLAMA_API, data=ollama_body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(o_req, timeout=50) as o_resp:
                ai_reply = json.loads(o_resp.read().decode()).get("response", "").strip()

            elapsed = round(time.time() - t0, 2)
            print(f"⚡ [INFERENCIA RESUELTA]: {len(ai_reply)} chars en {elapsed}s")

            comp_body = json.dumps({
                "job_id": job_id,
                "response": ai_reply,
                "model": chosen_model
            }).encode()

            c_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/complete", data=comp_body, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(c_req, timeout=5)
            print("📤 [ENTREGA A RENDER COMPLETADA]\n")

    except Exception:
        pass

    time.sleep(1.2)  # Sondeo rápido
