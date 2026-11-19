#!/usr/bin/env python3
"""
[OASIS STASIS TUNER — DARWIN / MACBOOK AIR]
Aplica los principios del Paper O (supresión UV de Araki, cota sub-Landauer ln φ
y estado adiabático Stasis) al entorno de usuario de macOS sin modificar SIP.
"""
import os
import shutil
import subprocess
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def main():
    print("=================================================================")
    print("❄️  OASIS STASIS TUNER — OPTIMIZACIÓN TÉRMICA MACBOOK AIR (DARWIN)")
    print("=================================================================")

    # 1. Evitar indexación Spotlight en carpetas de alta frecuencia (Supresión UV)
    for rel in [".git", ".lake"]:
        target = REPO / rel
        if target.is_dir():
            marker = target / ".metadata_never_index"
            marker.touch(exist_ok=True)
            print(f"  ✅ Supresión UV Spotlight activada en: {target}")

    # 2. Configurar variables de eficiencia de Ollama en ~/.zshrc si no existen
    zshrc = Path.home() / ".zshrc"
    content = zshrc.read_text(encoding="utf-8") if zshrc.exists() else ""
    additions = []
    if "OLLAMA_FLASH_ATTENTION" not in content:
        additions.append('export OLLAMA_FLASH_ATTENTION=1')
    if "OLLAMA_KEEP_ALIVE" not in content:
        additions.append('export OLLAMA_KEEP_ALIVE="2m"')

    if additions:
        with zshrc.open("a", encoding="utf-8") as f:
            f.write("\n# Oasis Stasis Thermal Bounds (Paper O)\n" + "\n".join(additions) + "\n")
        print("  ✅ Variables térmicas de Ollama añadidas a ~/.zshrc (Flash Attention + Keep-Alive 2m).")
    else:
        print("  ✅ Variables térmicas de Ollama ya configuradas en ~/.zshrc.")

    # 3. Limpiar artefactos temporales de compilación en /tmp
    cleaned = 0
    for tmp_item in Path("/tmp").glob("oasis_*"):
        if tmp_item.is_dir():
            shutil.rmtree(tmp_item, ignore_errors=True)
        else:
            tmp_item.unlink(missing_ok=True)
        cleaned += 1
    for tmp_dir in ["/tmp/audit_olean", "/tmp/paper_n_olean"]:
        p = Path(tmp_dir)
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)
            cleaned += 1
    print(f"  ✅ Limpieza de entropía residual en /tmp: {cleaned} artefactos eliminados.")

    # 4. Diagnóstico instantáneo de carga y memoria
    load = run("sysctl -n vm.loadavg")
    mem_pressure = run("memory_pressure | grep 'System-wide memory free percentage' || true")
    print(f"  📊 Carga CPU (1m/5m/15m): {load}")
    if mem_pressure:
        print(f"  📊 {mem_pressure}")
    print("=================================================================")

if __name__ == "__main__":
    main()
