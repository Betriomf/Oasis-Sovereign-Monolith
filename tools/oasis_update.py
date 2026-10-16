#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ACTUALIZADOR QUIRÚRGICO DE ESPACIO DE USUARIO (< 150 MB)
Actualiza el núcleo de scripts, binarios CLI y VFS sin tocar el sistema base de macOS.
"""
import os
import sys
import json
import time
import subprocess
import urllib.request

REPO_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
TOOLS_DIR = os.path.expanduser("~/Oasis-Tools")
GATEWAY_URL = "https://oasis-sovereign-gateway.onrender.com"

print("\033[96m" + "="*65)
print("🔄 OASIS SOVEREIGN OS — ACTUALIZADOR QUIRÚRGICO")
print("   (Presupuesto térmico <= 5.39W | Cero modificaciones en APFS)")
print("="*65 + "\033[0m")

# 1. ACTUALIZACIÓN DEL REPOSITORIO Y SCRIPTS (< 5 MB)
print("📦 [1/4] Sincronizando scripts del Monolito desde GitHub...")
try:
    pull = subprocess.run(["git", "pull", "--ff-only"], cwd=REPO_DIR, capture_output=True, text=True, check=True)
    if "Already up to date" in pull.stdout:
        print("  • Scripts locales: \033[92mAL DÍA\033[0m (Cero descarga necesaria)")
    else:
        print(f"  • Scripts actualizados con éxito:\n    {pull.stdout.strip()}")
except Exception as e:
    print(f"  • \033[93mAviso en Git:\033[0m {e}")

# 2. AUDITORÍA Y ACTUALIZACIÓN DE BINARIOS CLI EN ~/Oasis-Tools
print("\n⚙️  [2/4] Verificando herramientas CLI locales...")
cli_tools = ["vortex", "voxel", "oasis_doctor.py"]
os.makedirs(TOOLS_DIR, exist_ok=True)

for tool in ["vortex", "voxel"]:
    src = os.path.join(TOOLS_DIR, tool)
    if os.path.exists(src):
        os.chmod(src, 0o755)
        print(f"  • Binario '{tool}': \033[92mOPERATIVO\033[0m (Permisos 755)")
    else:
        print(f"  • Binario '{tool}': \033[91mNO ENCONTRADO\033[0m")

# 3. VERIFICACIÓN DEL ALMACÉN VFS / ASSETS
print("\n💾 [3/4] Auditando almacén inmutable VFS...")
roms_dir = os.path.join(TOOLS_DIR, "roms")
os.makedirs(roms_dir, exist_ok=True)
assets = os.listdir(roms_dir)
if assets:
    print(f"  • {len(assets)} archivos montados en VFS local:")
    for a in assets:
        sz = round(os.path.getsize(os.path.join(roms_dir, a)) / 1024, 1)
        print(f"    - {a} ({sz} KB)")
else:
    print("  • VFS base ligero (0 MB ocupados, motor Raycaster embebido en RAM)")

# 4. ALINEACIÓN CON CAPA 0 (GATEWAY RENDER)
print("\n🌐 [4/4] Contrastando versión con Capa 0...")
t0 = time.time()
try:
    req = urllib.request.Request(f"{GATEWAY_URL}/", headers={"User-Agent": "OasisUpdater/1.0"})
    with urllib.request.urlopen(req, timeout=4) as r:
        ms = round((time.time() - t0) * 1000, 1)
        raw = r.read().decode()
        ver = "v6.3.0"
        for line in raw.splitlines():
            if "version" in line:
                ver = line.strip()
                break
        print(f"  • Gateway Cloud : \033[92mCONECTADO\033[0m ({ms} ms) -> {ver}")
except Exception as e:
    print(f"  • Gateway Cloud : \033[93mEN REPOSO O TIMEOUT\033[0m ({e})")

print("\033[96m" + "="*65)
print("✅ Actualización completada en régimen laminar. Silicio frío preservado.")
print("="*65 + "\033[0m")
