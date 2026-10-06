#!/usr/bin/env python3
"""
OASIS LOCAL ENCLAVE — CÍRCULO NEGRO v3.1
Aislamiento estricto, consentimiento de CPU y protección térmica.
"""
import os
import json
import time
import subprocess
import urllib.request
import urllib.error

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
HW_KEY = "OASIS-HW-468F6F695BDB"

# CONFIGURACIÓN DE CONSENTIMIENTO
# False = Tu Mac SOLO procesa tus preguntas personales. Cero uso externo.
# True  = Tu Mac ayuda al enjambre cuando esté frío a cambio de créditos.
SWARM_DONATION_ENABLED = False

# LÍMITE TÉRMICO (Stefan-Boltzmann Threshold)
MAX_LOAD_THRESHOLD = 1.6

# BARRERA DE COULOMB: Lista blanca cerrada de comandos permitidos en host
HOST_WHITELIST = {
    "uname -a": "uname -srm",
    "uptime": "uptime",
    "ollama list": "ollama list",
    "sw_vers": "sw_vers"
}

print("=" * 65)
print("🛡️  [OASIS ENCLAVE: CÍRCULO NEGRO v3.1 ACTIVO]")
print(f"🔐 Huella de Hardware: {HW_KEY}")
print(f"⚡ Compartir CPU con el Enjambre: {'ACTIVADO' if SWARM_DONATION_ENABLED else 'DESACTIVADO (Privado)'}")
print("🧊 Freno Térmico: Máximo 2 hilos Ollama | Límite carga: 1.6")
print("=" * 65)

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
        # 1. Monitoreo térmico previo
        load_1m = os.getloadavg()[0]
        cpu_cold = load_1m < MAX_LOAD_THRESHOLD

        # 2. Heartbeat a Render
        hb_payload = json.dumps({
            "hw_key": HW_KEY,
            "cpu_cold": cpu_cold,
            "swarm_opt_in": SWARM_DONATION_ENABLED,
            "loadavg": round(load_1m, 2)
        }).encode()

        req = urllib.request.Request(
            f"{RENDER_URL}/v1/swarm/heartbeat",
            data=hb_payload,
            headers={"Content-Type": "application/json", "x-hw-key": HW_KEY}
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        task = data.get("task")
        if task:
            task_id = task.get("task_id")
            task_type = task.get("type")
            is_external = task.get("hw_target") != HW_KEY

            # Filtro de consentimiento y barrera térmica
            if is_external and (not SWARM_DONATION_ENABLED or not cpu_cold):
                # Rechazar tarea externa para proteger silicio
                time.sleep(1.5)
                continue

            # A. Inferencia de Lenguaje (Local y Segura)
            if task_type == "AI_INFERENCE":
                prompt = task.get("prompt", "")
                print(f"📥 [ENCLAVE] Inferencia para: '{prompt[:45]}...'")

                ollama_payload = json.dumps({
                    "model": "qwen2.5:0.5b" if "--fast" in prompt else "oasis-edge:1.5b",
                    "prompt": f"Responde conciso y en español: {prompt.replace('--fast','').strip()}",
                    "stream": False,
                    "keep_alive": "30m",
                    "options": {"temperature": 0.23, "num_predict": 120, "num_thread": 2}
                }).encode()

                o_req = urllib.request.Request(OLLAMA_API, data=ollama_payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(o_req, timeout=25) as o_resp:
                    ai_reply = json.loads(o_resp.read().decode()).get("response", "").strip()

                # Devolver resultado
                res_payload = json.dumps({
                    "task_id": task_id,
                    "model_used": "oasis-edge:1.5b",
                    "response": ai_reply
                }).encode()

                s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(s_req, timeout=5)
                print("📤 [ENCLAVE] Respuesta entregada a la terminal.\n")

            # B. Comandos de Host (Barrera de Coulomb)
            elif task_type == "HOST_EXEC":
                cmd_in = task.get("cmd", "").strip()
                if cmd_in in HOST_WHITELIST:
                    safe_cmd = HOST_WHITELIST[cmd_in]
                    output = subprocess.check_output(safe_cmd, shell=True).decode()
                    print(f"⚡ [HOST SEGURO]: '{safe_cmd}' ejecutado.")
                else:
                    output = f"🛑 [BARRERA DE COULOMB]: Comando '{cmd_in}' bloqueado por seguridad. Solo permitidos: {list(HOST_WHITELIST.keys())}"
                    print(f"⚠️ [BLOQUEO]: Intento no autorizado: {cmd_in}")

                res_payload = json.dumps({"task_id": task_id, "output": output}).encode()
                s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(s_req, timeout=5)

            # C. Auditoría Anti-Fraude (Golden Ticket)
            elif task_type == "GOLDEN_TICKET" and SWARM_DONATION_ENABLED:
                factors = resolver_golden_ticket(task.get("challenge", 1000000016000000063))
                print(f"🎯 [GOLDEN TICKET]: Silicio validado honesto -> {factors}\n")

    except urllib.error.URLError:
        time.sleep(2.0)
    except Exception as e:
        time.sleep(2.0)

    time.sleep(1.8)
