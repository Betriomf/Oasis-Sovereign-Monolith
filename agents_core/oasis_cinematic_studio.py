#!/usr/bin/env python3
"""
OASIS ADVANCED CINEMATIC STUDIO v2 (Pilar 189)
Render cinemático determinista: Fondo dinámico + Música en 432Hz + Locución HD
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO = REPO / "studio"
ASSETS = STUDIO / "assets"
OUT = STUDIO / "output"

ASSETS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
if not Path(FONT_PATH).exists():
    FONT_PATH = "/System/Library/Fonts/Monaco.ttf"

def compilar_master():
    print("=" * 75)
    print("🚀 [OASIS CINEMATIC STUDIO v2]: Producción cinemática en silicio frío...")
    print("=" * 75)

    audio_aiff = ASSETS / "audio_pro.aiff"
    audio_mp3 = ASSETS / "audio_pro.mp3"
    bgm_wav = ASSETS / "ambient_drone.wav"
    mixed_audio = ASSETS / "final_mixed_audio.mp3"
    master_video = OUT / "oasis_master_cinematico_pro.mp4"

    texto = (
        "El conocimiento universal no requiere la destruccion del soporte fisico. "
        "En Capa Cero, la termodinamica y la ciencia abierta demuestran que el universo calcula en frio. "
        "La informacion se preserva intacta sin peajes corporativos."
    )

    subprocess.run(["say", "-v", "Jorge", texto, "-o", str(audio_aiff)], check=False)
    if not audio_aiff.exists():
        subprocess.run(["say", texto, "-o", str(audio_aiff)])
    subprocess.run(["ffmpeg", "-y", "-i", str(audio_aiff), str(audio_mp3)], capture_output=True)

    cmd_bgm = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "sine=frequency=108:duration=20",
        "-f", "lavfi", "-i", "sine=frequency=216:duration=20",
        "-filter_complex", "[0:a][1:a]amix=inputs=2:weights=0.5 0.5,volume=0.08,afade=t=out:st=14:d=4[aout]",
        "-map", "[aout]",
        str(bgm_wav)
    ]
    subprocess.run(cmd_bgm, capture_output=True)

    cmd_mix = [
        "ffmpeg", "-y",
        "-i", str(audio_mp3),
        "-i", str(bgm_wav),
        "-filter_complex", "[0:a]volume=1.0[v];[1:a]volume=0.18[bg];[v][bg]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]",
        str(mixed_audio)
    ]
    subprocess.run(cmd_mix, capture_output=True)

    vf = (
        "color=c=0x060d1a:s=1280x720:d=20,"
        "drawbox=x=30:y=30:w=1220:h=660:color=0x58a6ff@0.4:t=2,"
        f"drawtext=fontfile='{FONT_PATH}':text='OASIS SOVEREIGN CINEMA':fontcolor=0x58a6ff:fontsize=34:x=70:y=80,"
        f"drawtext=fontfile='{FONT_PATH}':text='PRESERVACION DEL CONOCIMIENTO Y TERMODINAMICA':fontcolor=0xf0f6fc:fontsize=22:x=70:y=170,"
        f"drawtext=fontfile='{FONT_PATH}':text='E = kB * T * ln(phi) | Delta_S -> 0':fontcolor=0x2ea043:fontsize=28:x=70:y=270"
    )

    cmd_render = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", vf,
        "-i", str(mixed_audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(master_video)
    ]
    subprocess.run(cmd_render, capture_output=True)

    print("-" * 75)
    if master_video.exists():
        print(f"🎉 MASTER CINEMÁTICO LISTO: {master_video.relative_to(REPO)}")
        print("🚀 Abriendo reproductor...")
        subprocess.run(["open", str(master_video)])
    print("=" * 75)

if __name__ == "__main__":
    compilar_master()
