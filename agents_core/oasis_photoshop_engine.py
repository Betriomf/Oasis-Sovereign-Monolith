#!/usr/bin/env python3
"""
OASIS CLI PHOTOSHOP & EXTENDED VIDEO ENGINE v3 (Pilar 182)
Generador visual blindado: Tipografía nativa de macOS + Fondos vectoriales Lavfi
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import json
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO = REPO / "studio"
ASSETS = STUDIO / "assets"
OUT = STUDIO / "output"
SCRIPTS = STUDIO / "scripts"

ASSETS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

# Tipografía estándar garantizada en macOS
FONT_MACOS = "/System/Library/Fonts/Helvetica.ttc"
if not Path(FONT_MACOS).exists():
    FONT_MACOS = "/System/Library/Fonts/Monaco.ttf"

def sanitizar_texto(txt: str) -> str:
    """Elimina caracteres que rompen los filtros de FFmpeg."""
    return txt.replace("'", "").replace(":", " -").replace("\n", " ").replace("\\", "")

def compilar_video_blindado():
    print("=" * 75)
    print("🎨 [OASIS CLI PHOTOSHOP ENGINE v3]: Generando vídeo cinemático...")
    print("=" * 75)

    script_path = SCRIPTS / "script_einstein_rosen_video.json"
    if not script_path.exists():
        print("⚠️ Guion base no encontrado.")
        return

    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])

    clip_files = []
    for s in scenes:
        sid = s["scene_id"]
        texto = s["narrative"]
        
        audio_aiff = ASSETS / f"audio_scene_{sid}.aiff"
        audio_mp3 = ASSETS / f"audio_scene_{sid}.mp3"
        video_clip = ASSETS / f"clip_hd_{sid}.mp4"

        # 1. Sintetizar locución
        subprocess.run(["say", "-v", "Jorge", texto, "-o", str(audio_aiff)], check=False)
        if not audio_aiff.exists():
            subprocess.run(["say", texto, "-o", str(audio_aiff)])
        subprocess.run(["ffmpeg", "-y", "-i", str(audio_aiff), str(audio_mp3)], capture_output=True)

        # 2. Textos limpios para overlay
        t_header = sanitizar_texto(f"OASIS CAPA 0 - ESCENA {sid}")
        t_body = sanitizar_texto(texto[:50] + "...")
        t_eq = sanitizar_texto(s.get("ascii_art", "")[:40])

        # 3. Renderizar directamente el clip con fondo cinemático y texto integrado
        # Colores temáticos por escena
        colores_fondo = ["0x0d1117", "0x031625", "0x120d1a"]
        bg_col = colores_fondo[(sid - 1) % len(colores_fondo)]

        vf_filter = (
            f"color=c={bg_col}:s=1280x720:d=10,"
            f"drawbox=x=30:y=30:w=1220:h=660:color=0x58a6ff@0.4:t=3,"
            f"drawtext=fontfile='{FONT_MACOS}':text='{t_header}':fontcolor=0x58a6ff:fontsize=36:x=70:y=80,"
            f"drawtext=fontfile='{FONT_MACOS}':text='{t_body}':fontcolor=0xc9d1d9:fontsize=24:x=70:y=180,"
            f"drawtext=fontfile='{FONT_MACOS}':text='{t_eq}':fontcolor=0x2ea043:fontsize=28:x=70:y=280"
        )

        cmd_clip = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", vf_filter,
            "-i", str(audio_mp3),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(video_clip)
        ]
        
        res = subprocess.run(cmd_clip, capture_output=True)
        if video_clip.exists():
            clip_files.append(video_clip)
            print(f"  ✅ Escena {sid} renderizada con tarjeta visual y audio.")
        else:
            print(f"  ⚠️ Error en Escena {sid}: {res.stderr.decode('utf-8', errors='ignore')[:120]}")

    if not clip_files:
        print("❌ No se pudieron generar los clips individuales.")
        return

    # 4. Concatenación determinista
    concat_txt = ASSETS / "concat_v3.txt"
    concat_txt.write_text("\n".join([f"file '{c.resolve()}'" for c in clip_files]), encoding="utf-8")

    final_video = OUT / "oasis_video_cinematico_hd.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(final_video)
    ]
    subprocess.run(cmd_concat, capture_output=True)

    print("-" * 75)
    if final_video.exists():
        print(f"🎉 MASTER HD FINAL COMPILADO: {final_video.relative_to(REPO)}")
        print("🚀 Abriendo en tu reproductor...")
        subprocess.run(["open", str(final_video)])
    else:
        print(f"Abriendo clip individual 1: {clip_files[0]}")
        subprocess.run(["open", str(clip_files[0])])
    print("=" * 75)

if __name__ == "__main__":
    compilar_video_blindado()
