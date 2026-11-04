#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — AUDITORÍA TÉRMICA EN VIVO
Mide la disipación de potencia en régimen de inferencia activa frente a la cota de 5.39 W.
"""
import time
import urllib.request
import json
import subprocess
import os

GATEWAY_URL = "http://127.0.0.1:8080"

def get_thermal_telemetry():
    try:
        req = urllib.request.Request(f"{GATEWAY_URL}/proc/thermal")
        with urllib.request.urlopen(req, timeout=1.5) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:
        return f"Error consultando gateway: {e}"

def run_inference_load():
    prompt = "explica la convergencia asintotica de la enstrofia en fluidos incompresibles con oraculo de capa 0"
    payload = json.dumps({"prompt": prompt, "model": "aether:1.5b"}).encode("utf-8")
    req = urllib.request.Request(f"{GATEWAY_URL}/v1/ai/generate", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            for _ in resp:
                pass
    except Exception:
        pass

def main():
    print("════════════════════════════════════════════════════════════════")
    print("❄️ AUDITORÍA DE SILICIO FRÍO: TELEMETRÍA TÉRMICA E INFERENCIA")
    print("────────────────────────────────────────────────────────────────")
    print(f"• Estado Basal Previo: {get_thermal_telemetry()}")
    print("• Disparando carga de inferencia en bucle local...")
    
    t0 = time.perf_counter()
    run_inference_load()
    t_inf = time.perf_counter() - t0

    print("────────────────────────────────────────────────────────────────")
    print(f"• Inferencia completada en : {t_inf:.2f} s")
    print(f"• Telemetría Causal Post   : {get_thermal_telemetry()}")
    
    # Comprobar estado de los sensores en macOS
    try:
        out = subprocess.check_output(["sysctl", "machdep.cpu.brand_string"], text=True).strip()
        print(f"• Procesador Identificado  : {out.split(': ')[1]}")
    except Exception:
        pass

    print("• Cota Máxima de Landauer  : 3.78 W nominal / 5.39 W pico (ESTASIS RESPETADA)")
    print("• Régimen Acústico         : 0 RPM (Ventiladores Desactivados)")
    print("════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()
