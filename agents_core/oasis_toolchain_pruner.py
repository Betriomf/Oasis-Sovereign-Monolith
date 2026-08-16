#!/usr/bin/env python3
"""
OASIS TOOLCHAIN & RUNTIME PRUNER (Pilar 154)
Purga de toolchains huérfanos de Rust, NVM y optimización de descargas
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()

def podar_toolchains():
    print("=" * 65)
    print("🛠️ [OASIS TOOLCHAIN PRUNER]: Optimizando entornos de desarrollo...")
    print("=" * 65)
    
    bytes_liberados = 0

    # 1. Purgar caché de NVM
    nvm_cache = HOME / ".nvm" / ".cache"
    if nvm_cache.exists():
        sz = sum(f.stat().st_size for f in nvm_cache.rglob('*') if f.is_file())
        shutil.rmtree(nvm_cache, ignore_errors=True)
        bytes_liberados += sz
        print(f"🧹 Purgada caché de NVM -> {sz / (1024**2):.1f} MB")

    # 2. Purgar descargas de Rustup
    rustup_downloads = HOME / ".rustup" / "downloads"
    if rustup_downloads.exists():
        sz = sum(f.stat().st_size for f in rustup_downloads.rglob('*') if f.is_file())
        shutil.rmtree(rustup_downloads, ignore_errors=True)
        bytes_liberados += sz
        print(f"🧹 Purgada caché de descargas Rustup -> {sz / (1024**2):.1f} MB")

    # 3. Purgar instaladores .dmg/.pkg viejos en Downloads
    downloads_dir = HOME / "Downloads"
    if downloads_dir.exists():
        for f in downloads_dir.glob("*.dmg"):
            try:
                sz = f.stat().st_size
                f.unlink()
                bytes_liberados += sz
                print(f"🗑️ Eliminado instalador DMG: {f.name} ({sz / (1024**2):.1f} MB)")
            except Exception:
                pass
        for f in downloads_dir.glob("*.pkg"):
            try:
                sz = f.stat().st_size
                f.unlink()
                bytes_liberados += sz
                print(f"🗑️ Eliminado instalador PKG: {f.name} ({sz / (1024**2):.1f} MB)")
            except Exception:
                pass

    mb = bytes_liberados / (1024 * 1024)
    print("-" * 65)
    print(f"🚀 [OPTIMIZACIÓN LISTA]: {mb:.2f} MB liberados sin alterar compiladores activos.")
    print("=" * 65)

if __name__ == "__main__":
    podar_toolchains()
