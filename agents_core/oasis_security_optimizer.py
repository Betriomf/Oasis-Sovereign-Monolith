#!/usr/bin/env python3
"""
OASIS SECURITY & STORAGE OPTIMIZER (Pilar 143)
Auditoría de persistencia y compactación de base de datos Git
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def optimizar_repositorio():
    print("=" * 60)
    print("🛡️ [OASIS SECURITY & STORAGE OPTIMIZER]")
    print("=" * 60)

    # 1. Eliminar tarballs residuales
    tarball = REPO / "llama.cpp-master.tar.gz"
    if tarball.exists():
        sz = tarball.stat().st_size
        tarball.unlink()
        print(f"✅ Eliminado tarball redundante: llama.cpp-master.tar.gz ({sz / (1024*1024):.2f} MB)")

    # 2. Compactar y podar objetos muertos de Git (git prune / gc)
    print("📦 Compactando base de datos de objetos Git...")
    subprocess.run(["git", "gc", "--prune=now", "--aggressive"], cwd=REPO)
    print("✅ Git Garbage Collection completado con éxito.")

if __name__ == "__main__":
    optimizar_repositorio()
