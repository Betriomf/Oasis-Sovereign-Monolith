#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🛡️ OASIS STRATEGIC INTELLIGENCE: EVALUADOR DE NOTICIAS (CAPA 0)

import json
import subprocess
import os
import sys

def analizar_noticias_lincos(bloque_noticias):
    lincos_prompt = f"""
::START_LINCOS_FRAMEWORK::
[MODE]: STRATEGIC_EVALUATION
[TEMPERATURE]: 0.000
[CRITERIA]: 
  1. Herramientas de Inteligencia Estratégica (Anti-IA genérica).
  2. Priorizar el dolor del proceso sobre la tecnología.
  3. Verificación de datos estricta.
  4. Elevación de la ambición intelectual.

[INPUT_NEWS_STREAM]:
{bloque_noticias}

[TASK]: Evalúa este flujo de noticias. Filtra las alucinaciones comerciales. 
Devuelve exclusivamente descriptores estructurados LINCOS identificando el valor real del negocio.
::END_LINCOS_FRAMEWORK::
"""

    print("❄️ Transmitiendo bloque de noticias al nodo qwen2.5:lincos...")
    try:
        cmd = ["/Applications/Ollama.app/Contents/Resources/ollama", "run", "qwen2.5:lincos", lincos_prompt]
        resultado = subprocess.check_output(cmd).decode("utf-8")
        
        print("\n::START_LINCOS_RESPONSE::")
        print(resultado)
        print("::END_LINCOS_RESPONSE::")
        
        snapshot = {"NEWS_SNAPSHOT": bloque_noticias, "ANALYSIS": resultado}
        with open("core-engine/strategic_news_snapshot.json", "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        print("\n💎 STRATEGIC_VAL_CLOSED: Análisis guardado en core-engine/strategic_news_snapshot.json")
        
    except Exception as e:
        print(f"❌ Error en el bus de Ollama: {e}")

if __name__ == "__main__":
    noticias_ejemplo = "Noticia: Empresa de software lanza solución milagrosa de IA sin cambiar la estructura organizativa de sus clientes."
    analizar_noticias_lincos(noticias_ejemplo)
