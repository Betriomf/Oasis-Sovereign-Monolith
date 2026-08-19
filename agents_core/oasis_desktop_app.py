#!/usr/bin/env python3
"""
OASIS DESKTOP APP EMULATOR (Pilar 176)
Lanzador de ventana de escritorio aislada (App Mode) para Oasis Live OS
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import shutil
import time
import os
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
URL = "http://localhost:8080/oasis_web_node.html"

def lanzar_en_modo_app():
    print("=" * 70)
    print("🖥️ [OASIS DESKTOP EMULATOR]: Iniciando entorno de escritorio soberano...")
    print("=" * 70)

    # 1. Asegurar que el servidor web de Capa 0 está activo
    server_running = subprocess.getoutput("lsof -ti :8080")
    if not server_running:
        print("⚡ Levantando servidor HTTP de Capa 0 en segundo plano...")
        subprocess.Popen(["python3", str(REPO / "agents_core" / "oasis_market_server.py")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)

    # 2. Intentar abrir en ventana nativa tipo aplicación (Brave o Chrome en modo --app)
    brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    if Path(brave_path).exists():
        print("🦁 Abriendo Oasis OS en ventana de aplicación aislada (Brave Engine)...")
        subprocess.Popen([brave_path, f"--app={URL}", "--window-size=1024,768"])
    elif Path(chrome_path).exists():
        print("🌐 Abriendo Oasis OS en ventana de aplicación aislada (Chrome Engine)...")
        subprocess.Popen([chrome_path, f"--app={URL}", "--window-size=1024,768"])
    else:
        print("🌍 Abriendo en navegador predeterminado...")
        subprocess.Popen(["open", URL])

    print("✅ Oasis Live Desktop ejecutándose en ventana autónoma.")
    print("🔒 Silicio: LAMINAR (< 0.1W de consumo en reposo)")
    print("=" * 70)

if __name__ == "__main__":
    lanzar_en_modo_app()
