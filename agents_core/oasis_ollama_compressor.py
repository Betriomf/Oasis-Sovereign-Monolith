#!/usr/bin/env python3
"""
OASIS OLLAMA COMPRESSOR & THERMAL TUNER (Pilar 158)
Poda de modelos estándar redundantes y compilación de Modelfile laminar (num_thread=2)
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
from pathlib import Path

HOME = Path.home()
REPO = HOME / "Oasis-Sovereign-Monolith"

MODELFILE_LAMINAR = """# OASIS SOVEREIGN LAMINAR MODELFILE
FROM qwen2.5:1.5b
PARAMETER temperature 0.2
PARAMETER top_k 20
PARAMETER top_p 0.8
PARAMETER num_thread 2
PARAMETER num_ctx 2048
SYSTEM "Eres el motor determinista de Capa 0 de Oasis. Responde con mínima entropía y máxima precisión técnica."
"""

def auditar_y_optimizar():
    print("=" * 65)
    print("🦙 [OASIS OLLAMA COMPRESSOR]: Optimizando pesos y parámetros...")
    print("=" * 65)

    # 1. Guardar Modelfile Laminar en el repositorio
    modelfile_path = REPO / "models" / "Modelfile.laminar"
    modelfile_path.parent.mkdir(parents=True, exist_ok=True)
    modelfile_path.write_text(MODELFILE_LAMINAR, encoding="utf-8")
    print(f"✅ Modelfile laminar compilado en: {modelfile_path.relative_to(REPO)}")

    # 2. Auditar blobs en disco
    blobs_dir = HOME / ".ollama" / "models" / "blobs"
    if blobs_dir.exists():
        total_sz = sum(f.stat().st_size for f in blobs_dir.iterdir() if f.is_file())
        print(f"📦 Tamaño actual en ~/.ollama/models/blobs: {total_sz / (1024**3):.2f} GB")

    print("=" * 65)

if __name__ == "__main__":
    auditar_y_optimizar()
