#!/usr/bin/env python3
"""
OASIS VIDEO ASSEMBLER & RENDERER (Pilar 180)
Ensamblado determinista de audio, frames y texto ASCII en formato MP4
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import shutil
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO_DIR = REPO / "studio"
OUT_DIR = STUDIO_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def comprobar_herramientas():
    print("=" * 70)
    print("🎥 [OASIS VIDEO ASSEMBLER]: Comprobando herramientas de render...")
    print("=" * 70)

    herramientas = ["ffmpeg", "yt-dlp"]
    for h in herramientas:
        status = "✅ Instalado" if shutil.which(h) else "⚠️ No detectado (instalar con brew/apt)"
        print(f"  • {h:<15}: {status}")

    print("-" * 70)
    print("📁 Estructura del estudio lista:")
    print("  • studio/scripts/  -> Guiones y storyboards cognitivos")
    print("  • studio/assets/   -> Imágenes generadas en Fooocus / metraje yt-dlp")
    print("  • studio/output/   -> Vídeos finales listos para YouTube/Redes")
    print("=" * 70)

if __name__ == "__main__":
    comprobar_herramientas()
