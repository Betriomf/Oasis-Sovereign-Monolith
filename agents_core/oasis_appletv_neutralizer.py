#!/usr/bin/env python3
"""
OASIS APPLE TV & MEDIA STORAGE NEUTRALIZER (Pilar 145)
Purga de almacenamiento en contenedores TV y bloqueo de pre-fetch
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
from pathlib import Path

def neutralizar_tv():
    home = Path.home()
    rutas = [
        home / "Library" / "Caches" / "com.apple.TV",
        home / "Library" / "Caches" / "com.apple.AppleMediaServices"
    ]
    for r in rutas:
        if r.exists():
            shutil.rmtree(r, ignore_errors=True)
    
    subprocess.run(["defaults", "write", "com.apple.TV", "automaticDownloadsEnabled", "-bool", "false"], capture_output=True)
    subprocess.run(["defaults", "write", "com.apple.AppleMediaServices", "DisableMetrics", "-bool", "true"], capture_output=True)
    print("✅ Apple TV bloqueado: Cero descargas automáticas y sin consumo de disco.")

if __name__ == "__main__":
    neutralizar_tv()
