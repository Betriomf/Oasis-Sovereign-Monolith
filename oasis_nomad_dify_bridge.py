#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — NOMAD & DIFY BRIDGE (Capa 2 / DePIN)
Conecta el orquestador HashiCorp Nomad con Dify (143.8k★) y la Minería de Gradientes.

Autor: Mariano Panzano Caballé (@Betriomf)
"""

import json
import time

WALLET = "33zJ9jmWYWe6JmHuw8aHoJqKQGFqdz1qVE"
NOMAD_JOB_SPEC = {
    "Job": {
        "ID": "oasis-gradient-worker",
        "Name": "Oasis Local AI Agent (Freebuff)",
        "Type": "service",
        "Datacenters": ["oasis-barcelona-m1"],
        "TaskGroups": [
            {
                "Name": "gradient-miners",
                "Count": 1,
                "Tasks": [
                    {
                        "Name": "freebuff-miner",
                        "Driver": "raw_exec",
                        "Config": {
                            "command": "python3",
                            "args": ["oasis_gradient_node.py"]
                        },
                        "Resources": {
                            "CPU": 500,
                            "MemoryMB": 256
                        }
                    }
                ]
            }
        ]
    }
}

def generar_dify_llm_config():
    """Genera la configuración de proveedor local para Dify"""
    dify_config = {
        "provider": "oasis_sovereign_llm",
        "label": "Oasis Local AI (Freebuff/Æther)",
        "icon": "🌀",
        "models": [
            {
                "model": "qwen2.5:1.5b",
                "type": "llm",
                "context_window": 32768,
                "landauer_reduction": "30.6%",
                "thermal_power_target": "3.90W"
            }
        ],
        "endpoint": "http://localhost:11434/v1"
    }
    
    with open("dify_oasis_provider.json", "w") as f:
        json.dump(dify_config, f, indent=2)
    print("✅ [Dify Integration]: Configuración 'dify_oasis_provider.json' exportada.")

def generar_nomad_job():
    """Exporta la especificación de trabajo para HashiCorp Nomad"""
    with open("oasis_worker.nomad.json", "w") as f:
        json.dump(NOMAD_JOB_SPEC, f, indent=2)
    print("✅ [Nomad Orchestration]: Espec de trabajo 'oasis_worker.nomad.json' generada.")

def orquestar_sistema():
    print("🚀 [OASIS MONOLITH]: CONECTANDO NOMAD + DIFY + AGENTES LOCALES...")
    print("=" * 65)
    generar_nomad_job()
    generar_dify_llm_config()
    print("=" * 65)
    print(f"💰 Billetera Objetivo: {WALLET}")
    print("💎 Sistema preparado para entrenamiento local, inferencia en silicio frío y liquidación L2.")

if __name__ == "__main__":
    orquestar_sistema()
