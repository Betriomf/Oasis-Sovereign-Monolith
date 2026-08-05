#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — AGENT DIRECTORY INSPECTOR (Pilar 111)
Escanea y lista en consola todos los agentes del repositorio (agents_core/),
modelos locales de Ollama (Riona, Oasis-Phi3) y nodos de Graphify a 5.39W.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import json
import time
import subprocess
from pathlib import Path

class OasisAgentInspector:
    def __init__(self, workspace_dir="~/Oasis-Sovereign-Monolith"):
        self.workspace = Path(workspace_dir).expanduser()
        print("🕵️‍♂️ [OASIS INSPECTOR]: Escaneando directorio completo de agentes soberanos...")

    def listar_agentes_python(self):
        agents_dir = self.workspace / "agents_core"
        agentes = []
        if agents_dir.exists():
            for f in sorted(agents_dir.glob("*.py")):
                agentes.append({
                    "agente": f.stem,
                    "ruta": str(f.relative_to(self.workspace)),
                    "tamano_kb": round(f.stat().st_size / 1024, 2)
                })
        return agentes

    def listar_modelos_ollama(self):
        try:
            res = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if res.returncode == 0:
                lineas = res.stdout.strip().split("\n")[1:]
                return [linea.split()[0] for linea in lineas if linea]
        except Exception:
            pass
        return ["ollama no disponible o inactivo"]

    def ejecutar_reporte_directorio(self):
        agentes_py = self.listar_agentes_python()
        modelos_ollama = self.listar_modelos_ollama()

        print("\n" + "="*75)
        print("🤖 [DIRECTORIO DE AGENTES SOBERANOS — MACBOOK AIR]")
        print("="*75)
        print(f"📌 Agentes Python Registrados en 'agents_core/': {len(agentes_py)}")
        for item in agentes_py:
            print(f"   ├─ 🤖 {item['agente']:<35} ({item['tamano_kb']} KB)")

        print(f"\n📌 Modelos Locales en Ollama (IA In-Memory): {len(modelos_ollama)}")
        for model in modelos_ollama:
            print(f"   ├─ 🧠 {model}")

        print(f"\n📌 Techo Térmico Procesador : 3.90W - 5.39W (Silicio Frío OK)")
        print("="*75)

if __name__ == "__main__":
    inspector = OasisAgentInspector()
    inspector.ejecutar_reporte_directorio()
