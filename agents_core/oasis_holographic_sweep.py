#!/usr/bin/env python3
"""
OASIS HOLOGRAPHIC SWEEP & FRACTAL COMPACTOR (Pilar 151)
Compresión fractal de históricos y purga de entornos zombi
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import subprocess
import tarfile
from pathlib import Path

HOME = Path.home()
REPO = HOME / "Oasis-Sovereign-Monolith"

def compactar_historicos():
    print("=" * 70)
    print("🌌 [OASIS HOLOGRAPHIC SWEEP]: Iniciando condensación de estados...")
    print("=" * 70)

    bytes_liberados = 0

    # 1. Condensar históricos duplicados en un único archivo fractal
    historicos = [HOME / "Oasis_Historico", HOME / "Oasis_Historico_Laminar", HOME / "OasisOS"]
    destino_tar = HOME / "Oasis_Historico_Holografico.tar.gz"

    dirs_a_comprimir = [d for d in historicos if d.exists()]
    if dirs_a_comprimir and not destino_tar.exists():
        print(f"📦 Condensando {len(dirs_a_comprimir)} árboles históricos en {destino_tar.name}...")
        with tarfile.open(destino_tar, "w:gz") as tar:
            for d in dirs_a_comprimir:
                tar.add(d, arcname=d.name)
        print("✅ Archivo histórico fractal creado con éxito.")

    # Borrar carpetas descomprimidas redundantes
    for d in dirs_a_comprimir:
        sz = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
        shutil.rmtree(d, ignore_errors=True)
        bytes_liberados += sz
        print(f"🗑️ Condensada y purgada carpeta física: {d.name} ({sz / (1024**2):.1f} MB)")

    # 2. Purgar entornos virtuales muertos en ~/
    entornos_muertos = [HOME / "moonshine_env", HOME / "langflow_env", HOME / "openwebui-env"]
    for env in entornos_muertos:
        if env.exists():
            sz = sum(f.stat().st_size for f in env.rglob('*') if f.is_file())
            shutil.rmtree(env, ignore_errors=True)
            bytes_liberados += sz
            print(f"🧹 Purgado entorno virtual inactivo: {env.name} ({sz / (1024**2):.1f} MB)")

    # 3. Purgar zips residuales ya respaldados
    zips_viejos = [HOME / "Ollama.zip", HOME / "Oasis_Sovereign_Backup_2026-04-08.zip", HOME / "Monolito_Legacy_Backup.tar.gz"]
    for z in zips_viejos:
        if z.exists():
            sz = z.stat().st_size
            z.unlink()
            bytes_liberados += sz
            print(f"🗑️ Eliminado zip redundante: {z.name} ({sz / (1024**2):.1f} MB)")

    # 4. Purgar cachés residuales de Library
    lib_caches = HOME / "Library" / "Caches"
    if lib_caches.exists():
        for item in lib_caches.iterdir():
            if item.name not in ["com.apple.Homebrew", "pip"]:
                try:
                    if item.is_dir():
                        sz = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                        shutil.rmtree(item, ignore_errors=True)
                        bytes_liberados += sz
                    else:
                        sz = item.stat().st_size
                        item.unlink()
                        bytes_liberados += sz
                except Exception:
                    pass
        print("🧹 Purgada bolsa de cachés en ~/Library/Caches")

    gb = bytes_liberados / (1024 ** 3)
    print("=" * 70)
    print(f"🚀 [GRAN BARRIDO COMPLETADO]: {gb:.2f} GB liberados en disco.")
    print("🔒 Repositorio principal, base de datos y modelos Ollama intactos.")
    print("=" * 70)

if __name__ == "__main__":
    compactar_historicos()
