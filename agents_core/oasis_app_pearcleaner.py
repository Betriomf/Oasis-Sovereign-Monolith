#!/usr/bin/env python3
"""
OASIS OPEN APPCLEANER / PEARCLEANER ENGINE (Pilar 146)
Desinstalador profundo de aplicaciones y purga de contenedores residuales
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import shutil
import sys
from pathlib import Path

HOME = Path.home()

DIRECTORIOS_RESIDUOS = [
    HOME / "Library" / "Application Support",
    HOME / "Library" / "Caches",
    HOME / "Library" / "Containers",
    HOME / "Library" / "Preferences",
    HOME / "Library" / "Saved Application State",
    HOME / "Library" / "HTTPStorages",
    HOME / "Library" / "WebKit"
]

def calcular_tamano(p: Path) -> int:
    if not p.exists(): return 0
    if p.is_file(): return p.stat().st_size
    total = 0
    for root, _, files in os.walk(p):
        for f in files:
            try: total += (Path(root) / f).stat().st_size
            except Exception: pass
    return total

def auditar_y_limpiar_app(bundle_id_o_nombre: str, ejecutar_borrado: bool = False):
    print("=" * 65)
    print(f"🔍 [OASIS PEARCLEANER]: Buscando residuos de '{bundle_id_o_nombre}'...")
    print("=" * 65)

    coincidencias = []
    termino = bundle_id_o_nombre.lower()

    # 1. Buscar el bundle principal en /Applications y ~/Applications
    for app_dir in [Path("/Applications"), HOME / "Applications"]:
        if app_dir.exists():
            for app in app_dir.glob("*.app"):
                if termino in app.name.lower():
                    coincidencias.append(app)

    # 2. Buscar residuos en Library
    for dir_base in DIRECTORIOS_RESIDUOS:
        if dir_base.exists():
            for item in dir_base.iterdir():
                if termino in item.name.lower():
                    coincidencias.append(item)

    if not coincidencias:
        print(f"ℹ️ No se encontraron archivos vinculados a '{bundle_id_o_nombre}'.")
        return

    bytes_totales = 0
    for c in coincidencias:
        sz = calcular_tamano(c)
        bytes_totales += sz
        print(f"  • {c.relative_to(HOME) if str(c).startswith(str(HOME)) else c} ({sz / (1024*1024):.2f} MB)")

    print("-" * 65)
    mb = bytes_totales / (1024 * 1024)
    print(f"📦 Tamaño total asociado: {mb:.2f} MB")

    if ejecutar_borrado:
        for c in coincidencias:
            try:
                if c.is_dir(): shutil.rmtree(c, ignore_errors=True)
                else: c.unlink()
                print(f"🗑️ Eliminado: {c.name}")
            except Exception as e:
                print(f"⚠️ Error borrando {c.name}: {e}")
        print(f"✅ [ÉXITO]: {mb:.2f} MB purgados definitivamente del disco.")
    else:
        print("💡 Para eliminar estos archivos definitivamente, añade '--delete' al comando.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 agents_core/oasis_app_pearcleaner.py <nombre_o_bundle> [--delete]")
        print("Ejemplo: python3 agents_core/oasis_app_pearcleaner.py adobe")
    else:
        nombre = sys.argv[1]
        borrar = "--delete" in sys.argv
        auditar_y_limpiar_app(nombre, ejecutar_borrado=borrar)
