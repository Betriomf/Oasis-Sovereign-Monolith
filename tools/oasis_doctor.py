#!/usr/bin/env python3
"""
OASIS SOVEREIGN DOCTOR v1.0
Auditoría rápida del estado del sistema, puertos, Git y procesos en ejecución.
"""
import os
import sys
import socket
import subprocess

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0

def get_git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
        branch = subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()
        status = subprocess.check_output(["git", "status", "--porcelain"]).decode().strip()
        dirty = "⚠️ (Archivos modificados sin commit)" if status else "✅ (Limpio y al día)"
        return f"{branch} @ {commit} {dirty}"
    except Exception:
        return "Desconocido"

def get_running_pids(script_name):
    try:
        out = subprocess.check_output(["pgrep", "-f", script_name]).decode().strip().split()
        return out
    except Exception:
        return []

def main():
    print("=" * 68)
    print("🩺 OASIS SOVEREIGN OS — AUDITORÍA GENERAL DEL SISTEMA")
    print("=" * 68)
    
    # 1. Git
    print(f"📦 Estado del Repositorio : {get_git_info()}")

    # 2. Puertos clave
    p8080 = check_port(8080)
    p9091 = check_port(9091)
    p11434 = check_port(11434)
    print(f"🌐 Puerto 8080 (Gateway Web) : {'🟢 ACTIVO (http://localhost:8080)' if p8080 else '🔴 INACTIVO'}")
    print(f"📡 Puerto 9091 (P2P Mesh)    : {'🟢 ACTIVO' if p9091 else '⚪ EN ESPERA'}")
    print(f"🦙 Puerto 11434 (Ollama IA)  : {'🟢 ACTIVO' if p11434 else '⚪ APAGADO'}")

    # 3. Procesos en segundo plano
    gateways = get_running_pids("oasis_render_gateway.py")
    live_nodes = get_running_pids("oasis_darwin_live.py")
    print(f"⚙️  Procesos Gateway activos  : {len(gateways)} (PIDs: {', '.join(gateways) if gateways else 'Ninguno'})")
    print(f"⚙️  Nodos Darwin Live activos : {len(live_nodes)} (PIDs: {', '.join(live_nodes) if live_nodes else 'Ninguno'})")

    # 4. Archivos esenciales de Capa 0
    repo = os.path.expanduser("~/Oasis-Sovereign-Monolith")
    gw_ok = os.path.exists(os.path.join(repo, "agents_core/oasis_render_gateway.py"))
    cli_ok = os.path.exists(os.path.join(repo, "agents_core/oasis_darwin_cli.py"))
    print(f"📁 agents_core/oasis_render_gateway.py : {'✅ Presente' if gw_ok else '❌ Falta'}")
    print(f"📁 agents_core/oasis_darwin_cli.py    : {'✅ Presente' if cli_ok else '❌ Falta'}")
    print("=" * 68)

if __name__ == "__main__":
    main()
