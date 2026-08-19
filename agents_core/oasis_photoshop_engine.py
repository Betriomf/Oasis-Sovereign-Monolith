#!/usr/bin/env python3
"""
OASIS CLI PHOTOSHOP & EXTENDED VIDEO ENGINE (Pilar 182)
Composición visual determinista (estilo Photoshop CLI) + Ensamblado cinemático
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import json
import shutil
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO = REPO / "studio"
ASSETS = STUDIO / "assets"
OUT = STUDIO / "output"
SCRIPTS = STUDIO / "scripts"

ASSETS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def generar_frame_cinematico(scene_id: int, titulo: str, subtitulo: str, ecuacion: str, out_img: Path):
    """Genera un fondo visual de alta definición mediante FFmpeg/Lavfi."""
    # Crear tarjeta gráfica con degradado radial y texto superpuesto
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=0x06090e:s=1280x720:d=1",
        "-vf", (
            f"drawbox=y=0:color=0x0d1117@0.8:width=iw:height=ih:t=fill,"
            f"drawbox=x=40:y=40:w=1200:h=640:color=0x58a6ff@0.3:t=2,"
            f"drawtext=text='{titulo}':fontcolor=0x58a6ff:fontsize=36:x=80:y=90,"
            f"drawtext=text='{subtitulo}':fontcolor=0xc9d1d9:fontsize=22:x=80:y=160,"
            f"drawtext=text='{ecuacion}':fontcolor=0x2ea043:fontsize=26:x=80:y=240"
        ),
        "-frames:v", "1",
        str(out_img)
    ]
    subprocess.run(cmd, capture_output=True)

def compilar_video_extendido():
    print("=" * 75)
    print("🎨 [OASIS CLI PHOTOSHOP ENGINE]: Componiendo escenas cinemáticas...")
    print("=" * 75)

    script_path = SCRIPTS / "script_einstein_rosen_video.json"
    if not script_path.exists():
        print("⚠️ Guion base no encontrado.")
        return

    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])

    concat_list = []
    for s in scenes:
        sid = s["scene_id"]
        texto = s["narrative"]
        
        img_path = ASSETS / f"frame_scene_{sid}.png"
        audio_aiff = ASSETS / f"audio_scene_{sid}.aiff"
        audio_mp3 = ASSETS / f"audio_scene_{sid}.mp3"
        video_clip = ASSETS / f"clip_extended_{sid}.mp4"

        # 1. Composición de imagen estilo Photoshop
        ecuacion_txt = s.get("ascii_art", "").replace("\n", " ")
        generar_frame_cinematico(
            sid,
            f"ESCENA {sid}: OASIS SOVEREIGN LABS",
            texto[:60] + "...",
            ecuacion_txt[:50],
            img_path
        )

        # 2. Generación vocal local
        subprocess.run(["say", "-v", "Jorge", texto, "-o", str(audio_aiff)], check=False)
        if not audio_aiff.exists():
            subprocess.run(["say", texto, "-o", str(audio_aiff)])
        
        subprocess.run(["ffmpeg", "-y", "-i", str(audio_aiff), str(audio_mp3)], capture_output=True)

        # 3. Ensamblar clip sincronizado con la duración del audio
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
        concat_list.append(f"file '{video_clip.resolve()}'")
        print(f"  • Escena {sid} ensamblada con tarjeta gráfica y locución.")

    # Concatenar en máster final
    list_file = ASSETS / "concat_extended_list.txt"
    list_file.write_text("\n".join(concat_list), encoding="utf-8")

    final_video = OUT / "oasis_video_cinematico_hd.mp4"
    cmd_final = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(final_video)
    ]
    subprocess.run(cmd_final, capture_output=True)

    print("-" * 75)
    print(f"✅ VÍDEO CINEMÁTICO COMPILADO: {final_video.relative_to(REPO)}")
    print("🚀 Abriendo reproductor...")
    subprocess.run(["open", str(final_video)])
    print("=" * 75)

if __name__ == "__main__":
    compilar_video_extendido()
