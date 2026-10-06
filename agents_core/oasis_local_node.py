#!/usr/bin/env python3
"""
OASIS LOCAL SWARM AGENT
Mantiene el túnel reverso activo contra Render y procesa tareas locales.
"""
import os
import json
import time
import subprocess
import urllib.request

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
HW_KEY = "OASIS-HW-468F6F695BDB"
MODEL_DEFAULT = "oasis-edge:1.5b"

print("=" * 65)
print(f"🛰️  [OASIS LOCAL SWARM AGENT]: Iniciando túnel soberano")
print(f"🔐 Huella de Silicio: {HW_KEY}")
print(f"🧠 Modelo Local: {MODEL_DEFAULT} | Destino: {RENDER_URL}")
print("=" * 65)

def factorize_golden_ticket(n):
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

while True:
    try:
        # 1. Enviar latido (Heartbeat) y recoger trabajo pendiente
        hb_data = json.dumps({"hw_key": HW_KEY, "model": MODEL_DEFAULT}).encode()
        req = urllib.request.Request(
            f"{RENDER_URL}/v1/swarm/heartbeat",
            data=hb_data,
            headers={"Content-Type": "application/json", "x-hw-key": HW_KEY}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        task = data.get("task")
        if task:
            task_id = task.get("task_id")
            task_type = task.get("type")

            # Caso A: Inferencia LLM
            if task_type == "AI_INFERENCE":
                prompt = task.get("prompt", "")
                chosen_model = "qwen2.5:7b-instruct-q4_K_M" if "--7b" in prompt else MODEL_DEFAULT
                clean_p = prompt.replace("--7b", "").strip()

                print(f"📥 [INFERENCIA RECIBIDA] ID: {task_id} | Modelo: {chosen_model}")
                ollama_payload = json.dumps({
                    "model": chosen_model,
                    "prompt": f"Eres el asistente de Oasis OS. Responde de forma clara y directa.\n\nConsulta: {clean_p}",
                    "stream": False,
                    "keep_alive": "60m",
                    "options": {"temperature": 0.23, "num_predict": 200, "num_thread": 6}
                }).encode()

                o_req = urllib.request.Request(OLLAMA_API, data=ollama_payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(o_req, timeout=40) as o_resp:
                    ai_text = json.loads(o_resp.read().decode()).get("response", "").strip()

                # Devolver resultado a Render
                res_data = json.dumps({
                    "task_id": task_id,
                    "model_used": chosen_model,
                    "response": ai_text
                }).encode()
                s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(s_req, timeout=5)
                print("📤 [RESPUESTA ENTREGADA A LA WEB]\n")

            # Caso B: Ejecución nativa de comando (host <cmd>)
            elif task_type == "HOST_EXEC":
                cmd = task.get("cmd", "")
                print(f"⚡ [COMANDO LOCAL RECIBIDO]: {cmd}")
                try:
                    cmd_out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode()
                except subprocess.CalledProcessError as e:
                    cmd_out = e.output.decode()
                except Exception as e:
                    cmd_out = str(e)

                res_data = json.dumps({"task_id": task_id, "output": cmd_out}).encode()
                s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(s_req, timeout=5)
                print("📤 [SALIDA DE COMANDO ENTREGADA]\n")

            # Caso C: Golden Ticket (Auditoría anti-fraude)
            elif task_type == "GOLDEN_TICKET":
                num = task.get("challenge", 1000000016000000063)
                t0 = time.time()
                factors = factorize_golden_ticket(num)
                duration = round((time.time() - t0) * 1000, 2)
                print(f"🎯 [GOLDEN TICKET RESUELTO]: Factores {factors} en {duration}ms. Capacidad certificada.\n")

    except Exception:
        pass

    time.sleep(1.2)
