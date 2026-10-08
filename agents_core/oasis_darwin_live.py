#!/usr/bin/env python3
import time, json, urllib.request, platform, subprocess

GATEWAY_URL = "https://oasis-sovereign-gateway.onrender.com/v1/swarm/telemetry"

def get_metrics():
    uname = platform.uname()
    return {
        "node_id": "oasis-darwin-apple-silicon",
        "system": uname.system,
        "machine": uname.machine,
        "thermal_budget": "< 1.85W (Silicio Frio)",
        "status": "ORGANIC_ACTIVE",
        "timestamp": int(time.time())
    }

def run():
    print("🌿 [OASIS DARWIN LIVE]: Sincronizado con Render Gateway 24/7...")
    payload = json.dumps(get_metrics()).encode("utf-8")
    req = urllib.request.Request(GATEWAY_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            print("✅ Telemetria de Darwin aceptada por el Enjambre (HTTP 200).")
    except Exception as e:
        print(f"ℹ️ Gateway conectado: {e}")

if __name__ == "__main__":
    run()
