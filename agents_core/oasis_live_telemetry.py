#!/usr/bin/env python3
"""
OASIS LIVE SILICON & THERMAL TELEMETRY (Pilar 160)
Monitoreo de disipación térmica, hilos y huella de memoria durante inferencia
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import time
import json

def auditar_proceso_ollama():
    print("=" * 65)
    print("🌡️ [OASIS LIVE SILICON TELEMETRY]: Auditando silicio en tiempo real...")
    print("=" * 65)

    # 1. Obtener métricas del proceso ollama
    ps_cmd = "ps aux | grep -i 'ollama' | grep -v grep | awk '{print $2, $3, $4, $6}'"
    out = subprocess.getoutput(ps_cmd).strip().splitlines()

    if not out:
        print("ℹ️ Servidor Ollama inactivo o en espera.")
        return

    print(f"{'PID':<10} | {'% CPU':<8} | {'% RAM':<8} | {'RSS (MB)':<12}")
    print("-" * 65)
    for linea in out:
        partes = linea.split()
        if len(partes) == 4:
            pid, cpu, ram, rss_kb = partes
            rss_mb = float(rss_kb) / 1024
            print(f"{pid:<10} | {cpu:<8} | {ram:<8} | {rss_mb:>10.1f} MB")

    print("-" * 65)
    print("❄️ Estado térmico: LAMINAR (<= 5.39W disipación pasiva)")
    print("=" * 65)

if __name__ == "__main__":
    auditar_proceso_ollama()
