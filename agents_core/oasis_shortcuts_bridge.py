#!/usr/bin/env python3
"""
OASIS SHORTCUTS & AUTOMATOR BRIDGE (Pilar 152)
Conector determinista para automatizaciones nativas de macOS y notificaciones de sistema
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import sys
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def enviar_notificacion_macos(titulo: str, mensaje: str):
    script_apple = f'display notification "{mensaje}" with title "{titulo}" sound name "Glass"'
    subprocess.run(["osascript", "-e", script_apple], capture_output=True)

def ejecutar_accion(accion: str):
    if accion == "sweep":
        subprocess.run(["python3", str(REPO / "agents_core" / "oasis_holographic_sweep.py")])
        enviar_notificacion_macos("Oasis Sovereign Monolith", "🌌 Gran Barrido Holográfico completado con éxito.")
    elif accion == "dust":
        subprocess.run(["python3", str(REPO / "agents_core" / "oasis_dust_visualizer.py"), str(Path.home())])
    elif accion == "shield":
        subprocess.run(["python3", str(REPO / "agents_core" / "oasis_telemetry_shield.py")])
        enviar_notificacion_macos("Oasis Shield", "🛡️ Telemetría y servicios zombi neutralizados.")
    else:
        print("Acciones disponibles: sweep, dust, shield")

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "sweep"
    ejecutar_accion(arg)
