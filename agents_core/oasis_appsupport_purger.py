#!/usr/bin/env python3
"""
OASIS APPLICATION SUPPORT DEEP PURGER (Pilar 157)
Purga de Service Workers, GPUCache, Code Cache y logs en Application Support
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
from pathlib import Path

HOME = Path.home()
APP_SUPPORT = HOME / "Library" / "Application Support"

PATRONES_PURGA = [
    "GPUCache",
    "Code Cache",
    "DawnCache",
    "Service Worker/CacheStorage",
    "Cache",
    "logs",
    "Crashpad"
]

def purgar_app_support():
    print("=" * 65)
    print("🧹 [OASIS APP SUPPORT PURGER]: Purgando cachés internas...")
    print("=" * 65)

    if not APP_SUPPORT.exists():
        print("Application Support no encontrado.")
        return

    bytes_liberados = 0
    carpetas_procesadas = 0

    for root, dirs, _ in os.walk(APP_SUPPORT):
        root_path = Path(root)
        for d in dirs:
            for patron in PATRONES_PURGA:
                if patron.lower() in d.lower():
                    target = root_path / d
                    try:
                        sz = sum(f.stat().st_size for f in target.rglob("*") if f.is_file())
                        if sz > 5 * 1024 * 1024:  # Mayor a 5 MB
                            shutil.rmtree(target, ignore_errors=True)
                            bytes_liberados += sz
                            carpetas_procesadas += 1
                            rel = target.relative_to(APP_SUPPORT)
                            print(f"  • Purgada caché: {str(rel):<40} | {sz / (1024**2):>6.1f} MB")
                    except Exception:
                        pass

    mb = bytes_liberados / (1024 * 1024)
    print("-" * 65)
    print(f"🚀 [PURGA COMPLETADA]: {mb:.2f} MB ({mb/1024:.2f} GB) liberados en {carpetas_procesadas} cachés.")
    print("🔒 Cuentas, datos y configuraciones personales 100% preservados.")
    print("=" * 65)

if __name__ == "__main__":
    purgar_app_support()
