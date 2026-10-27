#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS OS — PUENTE DE TELEMETRÍA Y MODEL SOUP (v1.0.3)
Sube num_predict a 2048 tokens para permitir demostraciones formales completas.
"""
import os
import json
import urllib.request

def ask_aether_soup(user_query):
    vacuum_dir = os.path.expanduser("~/oasis_vacuum")
    manifest_path = os.path.join(vacuum_dir, "aether_soup_manifest.json")
    
    soup_info = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                soup_info = json.load(f)
        except Exception:
            pass

    system_prompt = (
        f"[SISTEMA OASIS OS - MODEL SOUP CONECTADO EN RAM]:\n"
        f"• Estado del Silicio: RÉGIMEN_ADIABÁTICO_<=_4.18W\n"
        f"• Ubicación de Trabajo: ~/oasis_vacuum (RAM Disk > 100 GB/s | 0 TBW)\n"
        f"• Integración de Pilares: 364 Pilares Verificados (Navier-Stokes, Landauer-Oasis, Lean 4)\n"
        f"• Manifiesto Activo: {soup_info.get('architecture', 'Model Soup Lineal Activo')}\n\n"
        f"Instrucción: Desarrolla respuestas formales, rigurosas y completas sin truncar el resultado."
    )

    payload = {
        "model": "oasis-aether-soup:1.5b",
        "prompt": f"{system_prompt}\n\nConsulta: {user_query}",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 2048  # Aumentado para pruebas largas
        }
    }

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as err:
        return f"🚨 Error al conectar con Ollama: {err}"

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Demuestra formalmente cómo el atractor decádico acota la enstrofía"
    print(ask_aether_soup(query))
