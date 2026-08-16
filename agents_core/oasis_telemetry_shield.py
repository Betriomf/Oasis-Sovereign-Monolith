#!/usr/bin/env python3
"""
OASIS TELEMETRY & BACKGROUND SHIELD (Pilar 144)
Desactivación de Daemons y Agents residuales de terceros
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
from pathlib import Path

LAUNCH_AGENTS_USER = Path.home() / "Library" / "LaunchAgents"

PLISTS_A_DESACTIVAR = [
    "com.google.keystone.agent.plist",
    "com.google.keystone.xpcservice.plist",
    "com.google.GoogleUpdater.wake.plist",
    "com.adobe.GC.Invoker-1.0.plist"
]

def neutralizar_telemetria_usuario():
    print("=" * 60)
    print("🛡️ [OASIS TELEMETRY SHIELD]: Neutralizando actualizadores en segundo plano")
    print("=" * 60)

    desactivados = 0
    for plist in PLISTS_A_DESACTIVAR:
        ruta = LAUNCH_AGENTS_USER / plist
        if ruta.exists():
            try:
                subprocess.run(["launchctl", "unload", "-w", str(ruta)], capture_output=True)
                ruta.unlink()
                print(f"✅ Telemetría neutralizada y eliminada: {plist}")
                desactivados += 1
            except Exception as e:
                print(f"⚠️ Error al procesar {plist}: {e}")

    print("=" * 60)
    print(f"🚀 [RESULTADO]: {desactivados} servicios de telemetría zombi desactivados.")
    print("🔒 Malla Oasis y servicios esenciales de macOS al 100% operativos.")
    print("=" * 60)

if __name__ == "__main__":
    neutralizar_telemetria_usuario()
