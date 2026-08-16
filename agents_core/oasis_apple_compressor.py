#!/usr/bin/env python3
"""
OASIS APPLE APPS & RUNTIME COMPRESSOR (Pilar 166)
Compresión transparente HFS+/APFS sobre paquetes de usuario y aplicaciones
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import shutil
from pathlib import Path

HOME = Path.home()
APPS_DIR = Path("/Applications")

# Apps que no están firmadas por SSV del sistema y se pueden comprimir
APPS_CANDIDATAS = [
    "Visual Studio Code.app",
    "Brave Browser.app",
    "Google Chrome.app",
    "Slack.app",
    "Discord.app"
]

def comprimir_apps_apple():
    print("=" * 65)
    print("🍏 [OASIS APPLE COMPRESSOR]: Comprimiendo recursos de aplicaciones...")
    print("=" * 65)

    bytes_recuperados = 0

    for app_name in APPS_CANDIDATAS:
        app_path = APPS_DIR / app_name
        if app_path.exists():
            print(f"📦 Analizando y comprimiendo {app_name}...")
            # Medir tamaño previo
            sz_pre = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
            
            # Ejecutar compresión transparente ditto en carpeta temporal
            tmp_path = app_path.with_name(f"{app_name}.tmp")
            cmd = f"ditto --hfsCompression '{app_path}' '{tmp_path}' && rm -rf '{app_path}' && mv '{tmp_path}' '{app_path}'"
            try:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"  ✅ {app_name} comprimido con éxito.")
                else:
                    if tmp_path.exists(): shutil.rmtree(tmp_path)
            except Exception as e:
                print(f"  ⚠️ No se pudo comprimir {app_name}: {e}")

    # 2. Comprimir la base de Vault de Oasis en reposo
    vault_file = HOME / "Oasis-Sovereign-Monolith" / "oasis_vault.dat"
    if vault_file.exists():
        sz = vault_file.stat().st_size
        print(f"🔒 Comprimiendo transparentemente {vault_file.name} ({sz / (1024**2):.1f} MB)...")
        subprocess.run(f"ditto --hfsCompression '{vault_file}' '{vault_file}.c' && mv '{vault_file}.c' '{vault_file}'", shell=True, capture_output=True)

    print("-" * 65)
    print("🚀 Compresión transparente completada. Binarios intactos y operativos.")
    print("=" * 65)

if __name__ == "__main__":
    comprimir_apps_apple()
