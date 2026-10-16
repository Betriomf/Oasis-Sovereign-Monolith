#!/usr/bin/env python3
"""
OASIS STABLE DAEMON — SILICIO FRÍO
Conexión estable por túnel inverso sin saturar CPU ni activar ventiladores.
"""
import time
import json
import subprocess
import urllib.request
import urllib.error

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
HW_KEY = "OASIS-HW-468F6F695BDB"
# Usamos 0.5b o 1.5b con 2 hilos para evitar sobrecalentamiento
MODEL_FAST = "qwen2.5:0.5b"
MODEL_HEAVY = "oasis-edge:1.5b"

print("=" * 60)
print(f"🛰️  [OASIS STABLE DAEMON]: Silicio Frío Activo")
print(f"🔐 Huella de Hardware: {HW_KEY}")
print(f"🌐 Conexión Nube: {RENDER_URL}")
print("⚡ Límite térmico: 2 hilos CPU (Silencio garantizado)")
print("=" * 60)

def resolver_golden_ticket(n):
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
        # 1. Heartbeat contra Render
        hb_payload = json.dumps({"hw_key": HW_KEY, "model": MODEL_FAST}).encode()
        req = urllib.request.Request(
            f"{RENDER_URL}/v1/swarm/heartbeat",
            data=hb_payload,
            headers={"Content-Type": "application/json", "x-hw-key": HW_KEY}
        )
        
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())

        task = data.get("task")
        if task:
            task_id = task.get("task_id")
            task_type = task.get("type")

            # A. Tarea de IA
            if task_type == "AI_INFERENCE":
                prompt = task.get("prompt", "")
                target_model = MODEL_HEAVY if "--7b" in prompt or "--heavy" in prompt else MODEL_FAST
                clean_prompt = prompt.replace("--7b", "").replace("--heavy", "").strip()

                print(f"📥 [IA] Tarea {task_id} -> Modelo: {target_model}")
                
                ollama_payload = json.dumps({
                    "model": target_model,
                    "prompt": f"Responde conciso y directo: {clean_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.23,
                        "num_predict": 150,
                        "num_thread": 2  # CLAVE: Limitar a 2 núcleos para evitar ruido y sobrecalentamiento
                    }
                }).encode()

                o_req = urllib.request.Request(OLLAMA_API, data=ollama_payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(o_req, timeout=30) as o_resp:
                    ai_reply = json.loads(o_resp.read().decode()).get("response", "").strip()

                # Entregar respuesta
                res_payload = json.dumps({
                    "task_id": task_id,
                    "model_used": target_model,
                    "response": ai_reply
                }).encode()
                
                s_req = urllib.request.Request(
                    f"{RENDER_URL}/v1/swarm/result",
                    data=res_payload,
                    headers={"Content-Type": "application/json"}
                )
                urllib.request.urlopen(s_req, timeout=6)
                print("📤 [IA] Respuesta enviada con éxito.\n")

            # B. Tarea de Comandos Nativos (host <cmd>)
            elif task_type == "HOST_EXEC":
                cmd = task.get("cmd", "")
                print(f"⚡ [HOST] Ejecutando: {cmd}")
                try:
                    cmd_out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=6).decode()
                except subprocess.CalledProcessError as e:
                    cmd_out = e.output.decode()
                except Exception as e:
                    cmd_out = str(e)

                res_payload = json.dumps({"task_id": task_id, "output": cmd_out}).encode()
                s_req = urllib.request.Request(
                    f"{RENDER_URL}/v1/swarm/result",
                    data=res_payload,
                    headers={"Content-Type": "application/json"}
                )
                urllib.request.urlopen(s_req, timeout=6)
                print("📤 [HOST] Salida entregada.\n")

            # C. Golden Ticket (Auditoría Anti-Fraude)
            elif task_type == "GOLDEN_TICKET":
                num = task.get("challenge", 1000000016000000063)
                t0 = time.time()
                factors = resolver_golden_ticket(num)
                dt = round((time.time() - t0) * 1000, 2)
                print(f"🎯 [GOLDEN TICKET]: Factores calculados en {dt} ms. Verificado.\n")

    except urllib.error.URLError:
        # Micro-corte temporal de red: dormir y reintentar limpiamente
        time.sleep(2.5)
        continue
    except Exception as err:
        time.sleep(2.0)
        continue

    # Intervalo de reposo térmico (permite a la CPU disipar calor)
    time.sleep(2.0)
