#!/usr/bin/env python3
"""
OASIS ASYNC DAEMON — DESACOPLAMIENTO DE LATIDO
El latido corre en un hilo independiente; Ollama no puede congelar la conexión.
"""
import time
import json
import threading
import subprocess
import urllib.request
import urllib.error

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
HW_KEY = "OASIS-HW-468F6F695BDB"
MODELO = "qwen2.5:0.5b"  # 0.5B para respuestas en <2s sin calentar el Mac

CURRENT_STATUS = "IDLE"
HOST_WHITELIST = {
    "uname -a": "uname -srm",
    "uptime": "uptime",
    "ollama list": "ollama list",
    "sw_vers": "sw_vers"
}

print("=" * 65)
print("🚀 [OASIS ASYNC NODE]: Latido desacoplado activo")
print(f"🔐 Huella de Silicio: {HW_KEY}")
print(f"⚡ Modelo Ultraligero: {MODELO} (2 hilos de CPU)")
print("=" * 65)

def ejecutar_inferencia_ollama(task_id, prompt):
    global CURRENT_STATUS
    CURRENT_STATUS = "BUSY"
    try:
        clean_prompt = prompt.replace("--fast", "").strip()
        payload = json.dumps({
            "model": MODELO,
            "prompt": f"Responde en una frase concisa: {clean_prompt}",
            "stream": False,
            "options": {"num_thread": 2, "num_predict": 100, "temperature": 0.23}
        }).encode()

        req = urllib.request.Request(OLLAMA_API, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            ai_text = json.loads(resp.read().decode()).get("response", "").strip()

        # Enviar resultado a Render
        res_data = json.dumps({
            "task_id": task_id,
            "model_used": MODELO,
            "response": ai_text
        }).encode()
        s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(s_req, timeout=4)
        print(f"✅ [TAREA COMPLETADA]: '{clean_prompt[:30]}...'")

    except Exception as e:
        print(f"⚠️ Inferencia abortada o excedió timeout: {e}")
    finally:
        CURRENT_STATUS = "IDLE"

def ejecutar_comando_host(task_id, cmd_in):
    if cmd_in in HOST_WHITELIST:
        try:
            output = subprocess.check_output(HOST_WHITELIST[cmd_in], shell=True, timeout=3).decode()
        except Exception as e:
            output = str(e)
    else:
        output = f"🛑 Comando '{cmd_in}' bloqueado por la Barrera de Coulomb."

    res_data = json.dumps({"task_id": task_id, "output": output}).encode()
    try:
        s_req = urllib.request.Request(f"{RENDER_URL}/v1/swarm/result", data=res_data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(s_req, timeout=4)
    except Exception:
        pass

# Bucle principal de sondeo y latido
while True:
    try:
        hb_data = json.dumps({
            "hw_key": HW_KEY,
            "status": CURRENT_STATUS,
            "model": MODELO
        }).encode()

        req = urllib.request.Request(
            f"{RENDER_URL}/v1/swarm/heartbeat",
            data=hb_data,
            headers={"Content-Type": "application/json", "x-hw-key": HW_KEY}
        )

        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())

        task = data.get("task")
        if task:
            task_id = task.get("task_id")
            task_type = task.get("type")

            if task_type == "AI_INFERENCE":
                # Lanzar en hilo separado para NO bloquear el siguiente latido
                threading.Thread(
                    target=ejecutar_inferencia_ollama,
                    args=(task_id, task.get("prompt", "")),
                    daemon=True
                ).start()

            elif task_type == "HOST_EXEC":
                threading.Thread(
                    target=ejecutar_comando_host,
                    args=(task_id, task.get("cmd", "")),
                    daemon=True
                ).start()

    except Exception:
        pass

    # Intervalo áureo de latido (~1.94s)
    time.sleep(1.94)
