#!/usr/bin/env python3
"""
OASIS SELECTIVE SAFE RECLAIMER (Pilar 149)
Purga controlada de bolsas desalineadas: cachés de build y entornos huérfanos
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import shutil
from pathlib import Path

HOME = Path.home()
REPO = HOME / "Oasis-Sovereign-Monolith"

def purgar_seguro():
    print("=" * 65)
    print("🧹 [OASIS SAFE RECLAIMER]: Ejecutando purga selectiva...")
    print("=" * 65)

    objetivos = [
        (HOME / ".npm", "Caché de Node (.npm)"),
        (HOME / ".cargo" / "registry", "Caché de Crates Rust (.cargo/registry)"),
        (REPO / "oasis-video-env", "Entorno virtual huérfano (oasis-video-env)"),
        (REPO / "MoneyPrinterTurbo", "Módulo pesado no alineado (MoneyPrinterTurbo)")
    ]

    bytes_recuperados = 0
    for ruta, desc in objetivos:
        if ruta.exists():
            # Calcular tamaño
            sz = 0
            if ruta.is_file(): sz = ruta.stat().st_size
            else:
                for f in ruta.rglob("*"):
                    try:
                        if f.is_file(): sz += f.stat().st_size
                    except Exception: pass
            
            try:
                if ruta.is_dir(): shutil.rmtree(ruta, ignore_errors=True)
                else: ruta.unlink()
                bytes_recuperados += sz
                print(f"✅ Purgado: {desc:<45} | {sz / (1024*1024):>8.1f} MB")
            except Exception as e:
                print(f"⚠️ No se pudo purgar {desc}: {e}")

    mb = bytes_recuperados / (1024 * 1024)
    print("-" * 65)
    print(f"🚀 [TOTAL RECUPERADO]: {mb:.2f} MB ({mb/1024:.2f} GB) liberados en disco.")
    print("🔒 Entorno activo (langflow_stable), Git y Vault intactos.")
    print("=" * 65)

if __name__ == "__main__":
    purgar_seguro()
