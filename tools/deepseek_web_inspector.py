#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS LIVE INSPECTOR — DEEPSEEK SYNTHETIC AUDITOR
Extrae el HTML servido, valida endpoints y consulta a DeepSeek sobre la salud de la UI.
"""
import urllib.request, json, os, sys

LOCAL_GW = "http://127.0.0.1:8080"
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# 1. Descargar la página web exacta que ve el navegador
try:
    with urllib.request.urlopen(f"{LOCAL_GW}/terminal", timeout=3.0) as r:
        html_served = r.read().decode("utf-8")
except Exception as e:
    print(f"❌ No se puede contactar con la terminal local: {e}")
    sys.exit(1)

# 2. Descargar telemetría del sistema
with urllib.request.urlopen(f"{LOCAL_GW}/v1/system/audit-report", timeout=3.0) as r:
    audit = json.loads(r.read().decode("utf-8"))

print("═" * 70)
print("🤖 INSPECTOR SINTÉTICO OASIS (DARWIN -> DEEPSEEK)")
print("═" * 70)
print(f"• Tamaño HTML servido : {len(html_served)} bytes")
print(f"• Kernel Reportado    : {audit['system']['os_kernel']}")
print(f"• Estado Silicio      : {audit['system']['silicon_thermal_watts']} W (Estable)")
print(f"• Nodos Detectados    : {audit['system']['active_nodes']}")

# 3. Enviar a DeepSeek si la API Key existe
if not DEEPSEEK_KEY:
    print("\n💡 Para que DeepSeek audite el código en vivo, exporta tu clave:")
    print("   export DEEPSEEK_API_KEY=\"sk-...\"")
    print("   python3 tools/deepseek_web_inspector.py")
else:
    print("\n📡 Enviando volcado de la terminal web a DeepSeek...")
    prompt = (
        "Eres el auditor senior de Oasis Sovereign OS. Revisa este fragmento del HTML servido "
        "y confirma si la estructura de modales (Three.js, PDF.js, Prompt) tiene errores de capas "
        "o bloqueos de teclado:\n\n"
        f"Telemetría: {json.dumps(audit)}\n"
        f"HTML Head & Prompt: {html_served[:2500]}"
    )
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
        data=json.dumps({
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }).encode("utf-8")
    )
    try:
        with urllib.request.urlopen(req, timeout=12.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("\n📋 DICTAMEN DE DEEPSEEK:")
            print(data["choices"][0]["message"]["content"])
    except Exception as err:
        print(f"⚠️ Error conectando con la API de DeepSeek: {err}")

print("═" * 70)
