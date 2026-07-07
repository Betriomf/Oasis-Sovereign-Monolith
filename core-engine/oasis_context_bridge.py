#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🛡️ NUCLEUS BRIDGE: UNIFICACIÓN DE CONTEXTO GITHUB + CRM

import os
import subprocess
import json

def extraer_registro_github():
    # Extraer los últimos 3 commits del Monolito para medir la velocidad de desarrollo
    try:
        cmd = ["git", "log", "-n", "3", "--pretty=format:%s (%h)"]
        logs = subprocess.check_output(cmd).decode("utf-8").split("\n")
        return logs
    except Exception:
        return ["No se detectó repositorio Git activo."]

def empaquetar_contexto_lincos():
    git_context = extraer_registro_github()
    
    # Simulación de la lectura de la tabla de Twenty CRM (Capa 22)
    crm_context = {
        "active_projects": ["Oasis-Sovereign-Monolith", "BrainMapp"],
        "system_status": "Laminar",
        "atractor_target": 2.3026
    }
    
    # Estructuración en Descriptores Geométricos LINCOS
    payload = {
        "::START_MATRIX_CONTEXT::": {
            "LAYER": 22,
            "GITHUB_SNAPSHOT": git_context,
            "CRM_METRICS": crm_context
        }
    }
    return json.dumps(payload, indent=2)

if __name__ == "__main__":
    print("💎 Consolidando bus de datos unificado...")
    contexto_puro = empaquetar_contexto_lincos()
    
    # Guardar snapshot de contexto para que Langflow o Dify lo consuman de inmediato
    with open("core-engine/live_context.json", "w") as f:
        f.write(contexto_puro)
        
    print("⚡ Snapshot inyectado con éxito en core-engine/live_context.json")
