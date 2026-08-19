#!/usr/bin/env python3
"""
OASIS CLI PHOTOSHOP & EXTENDED VIDEO ENGINE v2 (Pilar 182)
Composición determinista de tarjetas gráficas y renderizado MP4 garantizado
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import json
import os
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO = REPO / "studio"
ASSETS = STUDIO / "assets"
OUT = STUDIO / "output"
SCRIPTS = STUDIO / "scripts"

ASSETS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def generar_frame(scene_id: int, titulo: str, subtitulo: str, ecuacion: str, out_img: Path):
    """Genera fondo estético oscuro con cajas vectoriales y tipografía de alto contraste."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=0x06090e:s=1280x720:d=1",
        "-vf", (
            "drawbox=y=0:color=0x0d1117@0.8:width=iw:height=ih:t=fill,"
            "drawbox=x=30:y=30:w=1220:h=660:color=0x58a6ff@0.4:t=3,"
            f"drawtext=text='{titulo}':fontcolor=0x58a6ff:fontsize=34:x=70:y=80,"
            f"drawtext=text='{subtitulo}':fontcolor=0xc9d1d9:fontsize=22:x=70:y=160,"
            f"drawtext=text='{ecuacion}':fontcolor=0x2ea043:fontsize=28:x=70:y=240"
        ),
        "-frames:v", "1",
        str(out_img)
    ]
    subprocess.run(cmd, capture_output=True)

def compilar_video():
    print("=" * 75)
    print("🎨 [OASIS CLI PHOTOSHOP ENGINE]: Componiendo escenas cinemáticas...")
    print("=" * 75)

    script_path = SCRIPTS / "script_einstein_rosen_video.json"
    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])

    clip_files = []
    for s in scenes:
        sid = s["scene_id"]
        texto = s["narrative"]
        
        img_path = ASSETS / f"frame_scene_{sid}.png"
        audio_aiff = ASSETS / f"audio_scene_{sid}.aiff"
        audio_mp3 = ASSETS / f"audio_scene_{sid}.mp3"
        video_clip = ASSETS / f"clip_hd_{sid}.mp4"

        # 1. Componer imagen
        ecuacion = s.get("ascii_art", "").replace("\n", " ")[:45]
        generar_frame(
            sid,
            f"OASIS CAPA 0: ESCENA {sid}",
            texto[:55] + "...",
            ecuacion,
            img_path
        )

        # 2. Sintetizar voz
        subprocess.run(["say", "-v", "Jorge", texto, "-o", str(audio_aiff)], check=False)
        if not audio_aiff.exists():
            subprocess.run(["say", texto, "-o", str(audio_aiff)])
        subprocess.run(["ffmpeg", "-y", "-i", str(audio_aiff), str(audio_mp3)], capture_output=True)

        # 3. Renderizar clip individual
        cmd_clip = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_mp3),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(video_clip)
        ]
        subprocess.run(cmd_clip, capture_output=True)
        clip_files.append(video_clip)
        print(f"  • Escena {sid} renderizada con éxito.")

    # 4. Concatenación robusta re-codificada
    final_video = OUT / "oasis_video_cinematico_hd.mp4"
    inputs = []
    for c in clip_files:
        inputs.extend(["-i", str(c)])

    filter_complex = f"[0:v][0:a][1:v][1:a][2:v][2:a]concat=n={len(clip_files)}:v=1:a=1[outv][outa]"

    cmd_concat = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(final_video)
    ]
    subprocess.run(cmd_concat, capture_output=True)

    print("-" * 75)
    if final_video.exists():
        print(f"✅ VÍDEO CINEMÁTICO COMPILADO: {final_video.relative_to(REPO)}")
        print("🚀 Abriendo reproductor en tu pantalla...")
        subprocess.run(["open", str(final_video)])
    else:
        print("⚠️ Hubo un detalle en la concatenación. Abriendo el primer clip:")
        subprocess.run(["open", str(clip_files[0])])
    print("=" * 75)

if __name__ == "__main__":
    compilar_video()
