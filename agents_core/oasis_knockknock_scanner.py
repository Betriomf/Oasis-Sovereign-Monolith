#!/usr/bin/env python3
"""
OASIS KNOCKKNOCK SCANNER (Pilar 148)
Escáner de Persistencia, Duplicados Pesados y Bolsas de Almacenamiento Residual
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import subprocess
from pathlib import Path

HOME = Path.home()
REPO = HOME / "Oasis-Sovereign-Monolith"

def calcular_tamano(p: Path) -> int:
    if not p.exists():
        return 0
    if p.is_file():
        return p.stat().st_size
    total = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass
    return total

def escanear_persistencia_y_volumen():
    print("=" * 65)
    print("🚪 [OASIS KNOCKKNOCK SCANNER]: Auditando residuos y persistencia...")
    print("=" * 65)

    bolsas_candidatas = [
        HOME / ".npm",
        HOME / ".cargo" / "registry",
        HOME / "Library" / "Application Support" / "Slack",
        HOME / "Library" / "Application Support" / "Discord",
        HOME / "Library" / "Application Support" / "Code" / "Cache",
        HOME / "Library" / "Application Support" / "Code" / "CachedData",
        REPO / "oasis-video-env",
        REPO / "MoneyPrinterTurbo",
        HOME / "Downloads"
    ]

    print("\n📦 [BOLSAS DE ALMACENAMIENTO DETECTADAS]:")
    print("-" * 65)
    total_desalineado = 0
    for b in bolsas_candidatas:
        if b.exists():
            sz = calcular_tamano(b)
            if sz > 10 * 1024 * 1024:  # Mayor a 10 MB
                mb = sz / (1024 * 1024)
                total_desalineado += sz
                ruta_str = str(b.relative_to(HOME) if str(b).startswith(str(HOME)) else b)
                print(f"  • {ruta_str:<45} | {mb:>8.1f} MB")

    print("-" * 65)
    print(f"📊 Espacio potencialmente recuperable: {total_desalineado / (1024 * 1024):.2f} MB")

    print("\n🔍 [AUDITORÍA DE PERSISTENCIA (LaunchAgents)]: ")
    print("-" * 65)
    launch_dir = HOME / "Library" / "LaunchAgents"
    if launch_dir.exists():
        for plist in launch_dir.glob("*.plist"):
            print(f"  ⚡ {plist.name}")

    print("=" * 65)

if __name__ == "__main__":
    escanear_persistencia_y_volumen()
