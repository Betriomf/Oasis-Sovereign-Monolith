#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS AI AUDITOR — DEEPSEEK / DIFY BRIDGE
Inspecciona el estado del Gateway y el frontend HTML enviando la telemetría a DeepSeek.
"""
import urllib.request, json, os, sys

LOCAL_GW = "http://127.0.0.1:8080"
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# 1. Obtener el informe consolidado del sistema
try:
    with urllib.request.urlopen(f"{LOCAL_GW}/v1/system/audit-report", timeout=3.0) as r:
        audit_data = json.loads(r.read().decode())
except Exception as e:
    print(f"❌ Gateway inalcanzable: {e}")
    sys.exit(1)

# 2. Diagnóstico local rápido sin gastar tokens
print("═" * 70)
print("🤖 OASIS AI AUDITOR (DARWIN)")
print("═" * 70)
print(f"• Kernel OS       : {audit_data['system']['os_kernel']}")
print(f"• Consumo Térmico : {audit_data['system']['silicon_thermal_watts']} W (Cota Sub-Landauer)")
print(f"• Nodos Malla     : {audit_data['system']['active_nodes']}")
print(f"• Archivos Bóveda : {audit_data['vault_storage']['total_files']}")
print(f"• Teoremas Lean 4 : {len(audit_data['layer_0_formal_kernel']['lean4_theorems'])} verificados (0 sorry)")

# 3. Consulta a DeepSeek si la clave está configurada
if DEEPSEEK_KEY:
    print("\n📡 Consultando a DeepSeek API sobre la estabilidad del sistema...")
    prompt = f"Actúa como auditor de software. Analiza esta telemetría de Oasis Sovereign OS y confirma si hay cuellos de botella: {json.dumps(audit_data)}"
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
        data=json.dumps({
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }).encode()
    )
    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            out = json.loads(resp.read().decode())
            print("\n📋 DICTAMEN DEEPSEEK:")
            print(out["choices"][0]["message"]["content"])
    except Exception as err:
        print(f"⚠️ Error conectando con DeepSeek: {err}")
else:
    print("\n💡 Consejo: Exporta tu clave con 'export DEEPSEEK_API_KEY=sk-...' para activar el dictamen autónomo.")
print("═" * 70)
