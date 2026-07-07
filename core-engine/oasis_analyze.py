#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🌌 MOTOR DE ANÁLISIS COAXIAL: CONEXIÓN LIVE_CONTEXT -> QWEN2.5:LINCOS

import json
import subprocess

print("📥 Leyendo Snapshot de Contexto Real (core-engine/live_context.json)...")

try:
    with open("core-engine/live_context.json", "r") as f:
        data_context = f.read()
except FileNotFoundError:
    print("❌ ERROR: Snapshot de contexto no detectado. Corre primero python core-engine/oasis_context_bridge.py")
    exit(1)

# Construir el Prompt formal bajo restricciones LINCOS
lincos_prompt = f"""
::START_LINCOS_FRAMEWORK::
[MODE]: ANALYZE_METRIC
[ATRACTOR_TARGET]: 2.3026
[INPUT_DATA]: {data_context}

[TASK]: Evalúa la densidad informacional de los últimos cambios de Git subidos. 
Determina si los archivos creados (deploy_crm.sh y oasis_context_bridge.py) aproximan el sistema hacia el flujo laminar o si introducen Jitter debido al fallo de Docker. 
Responde únicamente con descriptores estructurados.
::END_LINCOS_FRAMEWORK::
"""

print("❄️ Inyectando matriz en el nodo local qwen2.5:lincos a temp=0.000...")

# Ejecutar inferencia local llamando al binario nativo de Ollama
try:
    cmd = ["/Applications/Ollama.app/Contents/Resources/ollama", "run", "qwen2.5:lincos", lincos_prompt]
    resultado = subprocess.check_output(cmd).decode("utf-8")
    print("\n::START_LINCOS_RESPONSE::")
    print(resultado)
    print("::END_LINCOS_RESPONSE::")
except Exception as e:
    print(f"❌ ERROR en el bus de Ollama: {e}")

