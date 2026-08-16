#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — DEEP KAKEYA CLEANER (Pilar 141)
Limpieza Profunda de Estados Efímeros y Cachés en macOS
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
REPO = HOME / "Oasis-Sovereign-Monolith"

def calcular_tamano(ruta: Path) -> int:
    total = 0
    if ruta.is_file():
        return ruta.stat().st_size
    for root, _, files in os.walk(ruta):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass
    return total

def purgar_directorio_seguro(dir_path: Path, nombre: str) -> int:
    if not dir_path.exists():
        return 0
    sz = calcular_tamano(dir_path)
    try:
        shutil.rmtree(dir_path, ignore_errors=True)
        print(f"🧹 Purgado: {nombre} -> {sz / (1024 * 1024):.2f} MB")
        return sz
    except Exception as e:
        print(f"⚠️ No se pudo purgar {nombre}: {e}")
        return 0

def ejecutar_limpieza_profunda():
    print("=" * 60)
    print("🚀 INICIANDO PURGA PROFUNDA DE RESIDUOS (KAKEYA CAPA 0)")
    print("=" * 60)
    
    bytes_totales = 0

    # 1. Cachés de desarrollo de Python y Cargo
    for p in REPO.rglob("__pycache__"):
        bytes_totales += purgar_directorio_seguro(p, "__pycache__")
    
    cargo_git_checkouts = HOME / ".cargo" / "git" / "checkouts"
    if cargo_git_checkouts.exists():
        bytes_totales += purgar_directorio_seguro(cargo_git_checkouts, "Cargo Git Checkouts")

    # 2. Caché de pip
    pip_cache = HOME / "Library" / "Caches" / "pip"
    if pip_cache.exists():
        bytes_totales += purgar_directorio_seguro(pip_cache, "Pip Cache")

    # 3. Archivos multimedia temporales residuales en raíz
    patrones_basura = [
        "temp_*.mp3", "temp_*.mp4", "tmp_*.mp3", "tmp_*.mp4",
        "ha_*.mp3", "hv_*.mp4", "hc_*.mp4", "*.log", "hf_concat.txt", "list.txt"
    ]
    for pat in patrones_basura:
        for f in REPO.glob(pat):
            try:
                sz = f.stat().st_size
                f.unlink()
                bytes_totales += sz
            except Exception:
                pass

    mb_totales = bytes_totales / (1024 * 1024)
    gb_totales = mb_totales / 1024

    print("=" * 60)
    if gb_totales >= 1.0:
        print(f"✅ [TOTAL PURGADO]: {gb_totales:.2f} GB liberados en disco.")
    else:
        print(f"✅ [TOTAL PURGADO]: {mb_totales:.2f} MB liberados en disco.")
    print("🔒 [ESTADO]: Modelos de IA, Monolito y datos de usuario intactos.")
    print("=" * 60)

if __name__ == "__main__":
    ejecutar_limpieza_profunda()
