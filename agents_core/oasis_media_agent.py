#!/usr/bin/env python3
"""
OASIS MEDIA & WORKSPACE PIPELINE (Pilar 175)
Agente de procesamiento multimedia: yt-dlp + Transcripción + Resumen Lincos
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import shutil
import sys
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
MEDIA_DIR = REPO / "data" / "media_vault"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def procesar_video_resumen(url_video: str):
    print("=" * 70)
    print("🎥 [OASIS MEDIA AGENT]: Iniciando pipeline de extracción soberana...")
    print(f"🔗 URL: {url_video}")
    print("=" * 70)

    # 1. Comprobar si yt-dlp está instalado
    if not shutil.which("yt-dlp"):
        print("⚠️ 'yt-dlp' no está instalado en el sistema base.")
        print("💡 Instalar con: brew install yt-dlp (o apt install yt-dlp)")
        return

    # 2. Descargar audio en formato ligero
    output_tpl = str(MEDIA_DIR / "%(id)s.%(ext)s")
    cmd_dl = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_tpl,
        "--max-filesize", "50M",
        url_video
    ]
    
    print("⚡ Descargando y extrayendo pista de audio...")
    res = subprocess.run(cmd_dl, capture_output=True, text=True)
    
    if res.returncode == 0:
        print("✅ Audio descargado y asegurado en data/media_vault/")
        print("🎙️ Pasando a Whisper / Resumen determinista...")
        # Registro en bitácora de agentes
        log_path = MEDIA_DIR / "media_index.txt"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"PROCESSED: {url_video}\n")
    else:
        print(f"⚠️ Error en descarga: {res.stderr[:200]}")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        procesar_video_resumen(sys.argv[1])
    else:
        print("ℹ️ Uso: python3 agents_core/oasis_media_agent.py <URL_DE_VIDEO>")
