#!/usr/bin/env python3
"""
OASIS MASSIVE PURGER (Pilar 142)
Limpieza de alta densidad: ~/.cache, ~/Library/Caches y temporales
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
CACHE_DIR = HOME / ".cache"
LIB_CACHE = HOME / "Library" / "Caches"

def get_dir_size(p: Path) -> int:
    total = 0
    if not p.exists(): return 0
    if p.is_file(): return p.stat().st_size
    for root, _, files in os.walk(p):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass
    return total

def purgar():
    print("=" * 60)
    print("🧹 [OASIS MASSIVE PURGER]: Liberando almacenamiento residual...")
    print("=" * 60)
    
    bytes_liberados = 0

    # 1. Purgar ~/.cache (Huggingface hub / torch / etc.)
    if CACHE_DIR.exists():
        sz = get_dir_size(CACHE_DIR)
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        bytes_liberados += sz
        print(f"✅ Purgada carpeta ~/.cache -> {sz / (1024*1024):.2f} MB")

    # 2. Purgar cachés de navegadores/apps en ~/Library/Caches (seguro)
    caches_especificas = [
        LIB_CACHE / "Homebrew",
        LIB_CACHE / "pip",
        LIB_CACHE / "yarn",
        LIB_CACHE / "npm"
    ]
    for c in caches_especificas:
        if c.exists():
            sz = get_dir_size(c)
            shutil.rmtree(c, ignore_errors=True)
            bytes_liberados += sz
            print(f"✅ Purgada {c.name} en Library/Caches -> {sz / (1024*1024):.2f} MB")

    gb = bytes_liberados / (1024 * 1024 * 1024)
    print("=" * 60)
    print(f"🚀 [ÉXITO TOTAL]: {gb:.2f} GB liberados en disco.")
    print("🔒 Repositorio, base de datos y modelos Ollama 100% protegidos.")
    print("=" * 60)

if __name__ == "__main__":
    purgar()
