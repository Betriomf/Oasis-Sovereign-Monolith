import urllib.request
import json
import time

URL = "https://oasis-sovereign-gateway.onrender.com/v1/game/vortex"

print("🤖 [SIMULADOR DE BOT]: Lanzando ráfaga periódica de 7 peticiones a intervalos idénticos (50 ms)...")

for i in range(1, 8):
    payload = json.dumps({
        "session_id": f"bot_burst_{i}",
        "x": 1.0, "y": 0.5, "z": 2.0, "t": 0.1
    }).encode("utf-8")
    
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-client-time": str(time.time())
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Petición {i}: HTTP 200 OK | Estado: {data.get('entropy_status')}")
    except urllib.error.HTTPError as e:
        err_msg = json.loads(e.read().decode("utf-8"))
        print(f"🚨 Petición {i}: HTTP {e.code} | Bloqueado: {err_msg.get('motivo')}")
    
    time.sleep(0.05)  # Intervalo fijo exacto (sin ruido humano)
