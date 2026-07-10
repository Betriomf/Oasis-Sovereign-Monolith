#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🧠 NUCLEUS INTERROGATOR: INYECCIÓN DE OMNI-CONTEXTO AL SILICIO LOCAL

import json
import subprocess
import sys

def preguntar_ia_local(pregunta_usuario):
    try:
        with open("core-engine/omni_context.json", "r", encoding="utf-8") as f:
            contexto_completo = f.read()
    except FileNotFoundError:
        print("❌ ERROR: Corre primero python core-engine/oasis_omnibus.py para empaquetar tus fuentes.")
        return

    # Prompt estructurado en formato LINCOS de baja entropía
    lincos_prompt = f"""
::START_LINCOS_FRAMEWORK::
[MODE]: KNOWLEDGE_RETRIEVAL
[ATRACTOR_TARGET]: 2.3026
[LOCAL_RESOURCES]: {contexto_completo}

[QUERY]: {pregunta_usuario}
Evalúa y responde la consulta cruzando de forma estricta los datos de mis papers, notas de Sources y el estado actual del repositorio Git bajo la métrica del flujo laminar. Responde usando únicamente descriptores estructurados.
::END_LINCOS_FRAMEWORK::
"""

    print("❄️ Transmitiendo buffer al nodo local qwen2.5:lincos...")
    try:
        cmd = ["/Applications/Ollama.app/Contents/Resources/ollama", "run", "qwen2.5:lincos", lincos_prompt]
        resultado = subprocess.check_output(cmd).decode("utf-8")
        print("\n::START_LINCOS_RESPONSE::")
        print(resultado)
        print("::END_LINCOS_RESPONSE::")
    except Exception as e:
        print(f"❌ Error en el bus de Ollama: {e}")

if __name__ == "__main__":
    # Pregunta patrón cruzada
    pregunta = "¿Detectas alguna desviación o Jitter entre mis notas de física y el último código del repositorio?"
    if len(sys.argv) > 1:
        pregunta = " ".join(sys.argv[1:])
    preguntar_ia_local(pregunta)
