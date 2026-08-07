#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — MAC LAMINAR OPTIMIZER & TAURI PURGER (Pilar 127)
1. Ejecuta la purga de target/ de Tauri y limpieza de caché unificada.
2. Mantiene la fricción de fase kappa_M en cero entropía.
3. Configura el LaunchDaemon de macOS para mantenimiento automático diario.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class MacLaminarOptimizer:
    def __init__(self):
        self.workspace = Path(".").expanduser()
        print("🌌🪶 [LAMINAR OPTIMIZER]: Iniciando purga profunda y armonización de espacio...")

    def purgar_target_tauri(self):
        rutas_target = [
            Path("~/OasisOS/oasis-quantum/src-tauri/target").expanduser(),
            Path("~/Oasis-Sovereign-Monolith/apps/desktop/src-tauri/target").expanduser()
        ]
        espacio_liberado = False
        for ruta in rutas_target:
            if ruta.exists():
                print(f"🧹 Purgando residuos pesados en: {ruta}")
                subprocess.run(f"rm -rf {ruta}", shell=True)
                espacio_liberado = True

        if not espacio_liberado:
            print("✨ El directorio target de Tauri ya está limpio y optimizado.")

    def generar_launchd_plist(self):
        plist_path = Path("~/Library/LaunchAgents/com.oasis.laminar.optimizer.plist").expanduser()
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.oasis.laminar.optimizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>{self.workspace.absolute()}/purge_entropy.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        plist_path.write_text(plist_content, encoding="utf-8")
        print(f"⚙️ Daemon Launchd creado en: {plist_path.relative_to(Path('~').expanduser())}")

if __name__ == "__main__":
    optimizer = MacLaminarOptimizer()
    optimizer.purgar_target_tauri()
    optimizer.generar_launchd_plist()
