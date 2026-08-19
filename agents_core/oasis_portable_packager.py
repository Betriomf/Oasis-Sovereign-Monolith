#!/usr/bin/env python3
"""
OASIS PORTABLE LIVE PACKAGER (Pilar 174)
Generador de paquetes Live-USB / Servidor Web Autónomo
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import tarfile
import shutil
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
OUT_DIR = REPO / "dist"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARCHIVOS_CORE = [
    "agents_core/oasis_hybrid_router.py",
    "agents_core/oasis_market_server.py",
    "agents_core/oasis_golden_kernel.py",
    "apps/oasis_web_node.html",
    "models/Modelfile.laminar",
    "docs/PAPER_ENTROPIC_TIME_LINCOS.md",
    "VERDAD_OASIS.txt"
]

SCRIPT_BOOT = """#!/usr/bin/env bash
# OASIS LIVE AUTO-BOOTSTRAP (Portátil / Tails / Web Server)
echo "====================================================="
echo "🌌 INICIANDO OASIS PORTABLE SOVEREIGN NODE"
echo "====================================================="

# 1. Iniciar Ollama si está disponible
if command -v ollama >/dev/null 2>&1; then
    echo "⚡ Iniciando runtime local en segundo plano..."
    OLLAMA_ORIGINS="*" OLLAMA_NUM_PARALLEL=1 ollama serve >/dev/null 2>&1 &
    sleep 2
    if ! ollama list | grep -q "oasis-laminar:1.5b"; then
        echo "🦙 Compilando modelo laminar..."
        ollama create oasis-laminar:1.5b -f models/Modelfile.laminar
    fi
fi

# 2. Levantar el Servidor Web Híbrido
echo "🚀 Levantando servidor web en http://localhost:8080..."
python3 agents_core/oasis_market_server.py
"""

def empaquetar_oasis_live():
    print("=" * 65)
    print("📦 [OASIS PORTABLE PACKAGER]: Empaquetando sistema autónomo...")
    print("=" * 65)

    staging = OUT_DIR / "oasis_portable"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    # 1. Copiar componentes clave
    for item in ARCHIVOS_CORE:
        src = REPO / item
        dst = staging / item
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  • Incluido: {item}")

    # 2. Generar script de arranque autónomo
    boot_file = staging / "oasis_boot.sh"
    boot_file.write_text(SCRIPT_BOOT, encoding="utf-8")
    boot_file.chmod(0o755)
    print("  • Generado: oasis_boot.sh (Ejecutable universal)")

    # 3. Comprimir a formato .tar.gz para pendrive o servidor
    tar_path = OUT_DIR / "oasis_portable_live.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(staging, arcname="oasis_portable")

    tam_mb = tar_path.stat().st_size / (1024 * 1024)
    print("-" * 65)
    print(f"✅ Paquete autónomo compilado en: dist/oasis_portable_live.tar.gz ({tam_mb:.2f} MB)")
    print("💾 Listo para copiar a cualquier Pendrive USB o servidor web público.")
    print("=" * 65)

if __name__ == "__main__":
    empaquetar_oasis_live()
