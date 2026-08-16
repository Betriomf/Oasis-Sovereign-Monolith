#!/usr/bin/env python3
"""
OASIS APFS TRANSPARENT COMPRESSOR (Pilar 165)
Compresión transparente LZVN/ZLIB a nivel de bloques APFS sin romper ejecutables
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import os
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def comprimir_arbol_apfs(ruta_objetivo: Path):
    print("=" * 65)
    print(f"🗜️ [OASIS APFS COMPRESSOR]: Aplicando compresión nativa en '{ruta_objetivo.name}'...")
    print("=" * 65)

    if not ruta_objetivo.exists():
        print("Ruta no encontrada.")
        return

    # Usar afscexpress si existe, o ditto con compresión HFS+/APFS
    cmd = f"ditto --hfsCompression '{ruta_objetivo}' '{ruta_objetivo}_compressed' && rm -rf '{ruta_objetivo}' && mv '{ruta_objetivo}_compressed' '{ruta_objetivo}'"
    
    print("⚡ Comprimiendo bloques de datos de forma transparente...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if res.returncode == 0:
        print("✅ Compresión APFS completada con éxito.")
        print("🔒 Los archivos siguen siendo ejecutables y legibles de forma transparente.")
    else:
        print(f"⚠️ Error durante la compresión: {res.stderr}")
    print("=" * 65)

if __name__ == "__main__":
    comprimir_arbol_apfs(REPO / "agents_core")
