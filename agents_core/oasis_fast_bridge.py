#!/usr/bin/env python3
import urllib.request, json, time

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "oasis-edge:1.5b"

print(f"🛰️  [ENLACE ACTIVO]: {RENDER_URL} <---> Ollama ({MODEL})")

# Test inicial directo a Ollama
try:
    test_req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps({"model": MODEL, "prompt": "test", "stream": False}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(test_req, timeout=10) as r:
        print("✅ [OLLAMA LOCAL ONLINE]: Respondiendo correctamente en silicio frío.\n")
except Exception as e:
    print(f"❌ [ERROR OLLAMA]: Asegúrate de que Ollama está abierto. Detalle: {e}\n")

while True:
    try:
        req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/poll")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        
        if data.get("has_job"):
            job_id = data["job_id"]
            prompt = data["prompt"]
            print(f"📥 [PROMPT]: {prompt[:50]}...")
            
            # Inferencia rápida
            o_req = urllib.request.Request(
                OLLAMA_URL,
                data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(o_req, timeout=30) as o_resp:
                reply = json.loads(o_resp.read().decode()).get("response", "").strip()

            # Envío a Render
            c_req = urllib.request.Request(
                f"{RENDER_URL}/v1/swarm/complete",
                data=json.dumps({"job_id": job_id, "response": reply, "model": MODEL}).encode(),
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(c_req, timeout=5)
            print("📤 [RESPUESTA ENTREGADA A LA WEB]\n")
    except Exception:
        pass
    time.sleep(1.0)
