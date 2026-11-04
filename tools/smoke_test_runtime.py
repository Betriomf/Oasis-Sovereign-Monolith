#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — SMOKE TEST DE RUNTIME (GITOPS INTEGRITY)
Verifica que Ollama y la cascada de Riona estén operativos antes de autorizar despliegues.
"""
import urllib.request
import sys
import os

sys.path.insert(0, os.path.expanduser("~/Oasis-Sovereign-Monolith/agents_core"))
import riona_agent

def check_ollama():
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False

def check_riona():
    res = riona_agent.riona_process("noticias de ciencia")
    return "TITULARES" in res or "RESULTADOS" in res or "GITHUB" in res

if __name__ == "__main__":
    ollama_ok = check_ollama()
    riona_ok = check_riona()

    print("════════════════════════════════════════════════════════════════")
    print("🔍 GITOPS RUNTIME HEALTH-CHECK (ESTABILIDAD Y RESILIENCIA)")
    print("────────────────────────────────────────────────────────────────")
    print(f"• Motor Ollama (11434)   : {'✅ OPERATIVO' if ollama_ok else '⚠️ DETENIDO (Requiere ollama serve)'}")
    print(f"• Cascada Riona (Web/RSS): {'✅ OPERATIVO' if riona_ok else '⚠️ FALLO EN SCRAPING'}")
    print("════════════════════════════════════════════════════════════════")

    # Si Riona está completamente ciego, advertir al entorno
    if not riona_ok:
        sys.exit(1)
    sys.exit(0)
