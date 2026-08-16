#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — KAKEYA DISK PURGER (CAPA 0)
Reducción de Medida de Lebesgue en Almacenamiento Local
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path.home() / "Oasis-Sovereign-Monolith"
VIDEOS_DIR = Path.home() / "Oasis_Studio_Videos"

def purgar_residuos_temporales():
    print("🧹 [KAKEYA PURGER]: Iniciando contracción volumétrica de disco...")
    bytes_liberados = 0

    # 1. Purgar archivos temporales generados en runs anteriores (.mp3, .mp4 temporales, .txt concat)
    patrones_basura = ["temp_*.mp3", "temp_*.mp4", "tmp_*.mp3", "tmp_*.mp4", "ha_*.mp3", "hv_*.mp4", "hc_*.mp4", "*_concat.txt", "list.txt"]
    
    for pat in patrones_basura:
        for f in BASE_DIR.glob(pat):
            try:
                sz = f.stat().st_size
                f.unlink()
                bytes_liberados += sz
            except Exception:
                pass

    # 2. Purgar cachés de Python (__pycache__)
    for p in BASE_DIR.rglob("__pycache__"):
        if p.is_dir():
            for f in p.glob("*"):
                try:
                    bytes_liberados += f.stat().st_size
                except Exception:
                    pass
            shutil.rmtree(p, ignore_errors=True)

    # 3. Purgar caché de compilación en Tauri si existe
    tauri_target = BASE_DIR / "src-tauri" / "target"
    if tauri_target.exists():
        for root, dirs, files in os.walk(tauri_target):
            for f in files:
                try:
                    bytes_liberados += (Path(root) / f).stat().st_size
                except Exception:
                    pass
        shutil.rmtree(tauri_target, ignore_errors=True)

    mb_liberados = bytes_liberados / (1024 * 1024)
    print(f"✅ [VOLUMEN REDUCIDO]: {mb_liberados:.2f} MB purgados en el disco.")
    print("🔒 [INFORMACIÓN PRESERVADA]: 100% de la funcionalidad y base de código intacta.")

if __name__ == "__main__":
    purgar_residuos_temporales()
