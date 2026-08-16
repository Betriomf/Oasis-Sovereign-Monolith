#!/usr/bin/env python3
"""
OASIS NVM & RUSTUP LEAN OPTIMIZER (Pilar 155)
Purga determinista de versiones obsoletas de Node y documentación pesada de Rust
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import shutil
import subprocess
from pathlib import Path

HOME = Path.home()

def optimizar_runtimes():
    print("=" * 65)
    print("⚡ [OASIS RUNTIME LEAN]: Purgando versiones huérfanas de Node y Rust...")
    print("=" * 65)

    bytes_recuperados = 0

    # 1. Auditar y purgar carpetas de versiones viejas en NVM
    nvm_nodes = HOME / ".nvm" / "versions" / "node"
    if nvm_nodes.exists():
        versiones = sorted([d for d in nvm_nodes.iterdir() if d.is_dir()], key=lambda x: x.name)
        if len(versiones) > 1:
            activa = versiones[-1]  # Conservar la más reciente
            print(f"🔒 Conservando versión principal: {activa.name}")
            for v in versiones[:-1]:
                sz = sum(f.stat().st_size for f in v.rglob('*') if f.is_file())
                shutil.rmtree(v, ignore_errors=True)
                bytes_recuperados += sz
                print(f"🗑️ Purgada versión huérfana: {v.name} ({sz / (1024**2):.1f} MB)")

    # 2. Purgar docs locales de rustup si existen
    rust_docs = HOME / ".rustup" / "toolchains" / "stable-x86_64-apple-darwin" / "share" / "doc"
    if rust_docs.exists():
        sz = sum(f.stat().st_size for f in rust_docs.rglob('*') if f.is_file())
        shutil.rmtree(rust_docs, ignore_errors=True)
        bytes_recuperados += sz
        print(f"🧹 Purgada documentación local de Rust -> {sz / (1024**2):.1f} MB")

    mb = bytes_recuperados / (1024 * 1024)
    print("-" * 65)
    print(f"🚀 [RECUPERACIÓN COMPLETADA]: {mb:.2f} MB liberados en runtimes.")
    print("=" * 65)

if __name__ == "__main__":
    optimizar_runtimes()
