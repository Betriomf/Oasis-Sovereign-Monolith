#!/usr/bin/env python3
"""
OASIS HYBRID VIDEO DIRECTOR (Pilar 180)
Motor de guionización cognitiva y producción multimedia basada en Open Science
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import json
import time
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"
STUDIO_DIR = REPO / "studio"
SCRIPTS_DIR = STUDIO_DIR / "scripts"
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

def generar_guion_cognitivo(tema: str, doi_o_paper: str = "Barontini 2026 / Einstein-Rosen"):
    print("=" * 75)
    print("🎬 [OASIS VIDEO DIRECTOR]: Diseñando guion cognitivo multimodal...")
    print(f"📖 Tema: {tema} | Referencia: {doi_o_paper}")
    print("=" * 75)

    guion = {
        "metadata": {
            "title": f"Misterio Revelado: {tema}",
            "reference": doi_o_paper,
            "created_at": int(time.time()),
            "aesthetic": "Textfiles ASCII + Fooocus Photorealistic Lensing"
        },
        "cognitive_framework": {
            "hebb_rule": "Sincronización exacta de fonemas Whisper con overlays tipográficos",
            "yerkes_dodson": "Pico de atención a 0:00 (Hook), calma a 0:45 (Explicación), clímax a 1:30",
            "ikea_effect": "Micro-reto de deducción en pantalla a 1:00",
            "pratfall_effect": "Desmontaje de la paradoja clásica inicial"
        },
        "scenes": [
            {
                "scene_id": 1,
                "timestamp": "00:00 - 00:15",
                "narrative": "¿Qué pasaría si el tiempo no existiera fuera de tu propia mente? Un puente de Einstein-Rosen lo cambia todo.",
                "fooocus_prompt": "Cinematic gravitational lens Einstein cross glowing cyan neon, ascii matrix overlay, 8k render, photorealistic, Unreal Engine 5 style",
                "ascii_art": "  +---+ \n  | E | \n+-+-+-+-+\n| R | O | S |\n+-+-+-+-+\n  | N | \n  +---+"
            },
            {
                "scene_id": 2,
                "timestamp": "00:15 - 00:45",
                "narrative": "En 2026, átomos ultra-fríos demostraron que el tiempo se detiene cuando la entropía se congela.",
                "fooocus_prompt": "Bose-Einstein condensate of rubidium atoms freezing in deep space, cold crystal blue light, sharp focus, hyperdetailed",
                "ascii_art": " [ 24,000 ATOMS ] ---> [ Delta_S -> 0 ] ---> [ STASIS ]"
            },
            {
                "scene_id": 3,
                "timestamp": "00:45 - 01:15",
                "narrative": "La cota de Landauer en régimen de Fibonacci ahorra un 30.58% de disipación térmica. El universo calcula en frío.",
                "fooocus_prompt": "Golden ratio spiral geometry made of glowing optical fibers in dark laboratory, mathematical equation floating in air, 4k",
                "ascii_art": "  E = kB * T * ln(phi) = 1.9932e-21 J"
            }
        ]
    }

    out_file = SCRIPTS_DIR / "script_einstein_rosen_video.json"
    out_file.write_text(json.dumps(guion, indent=2), encoding="utf-8")
    
    print(f"✅ Guion y Storyboard exportados en: {out_file.relative_to(REPO)}")
    print("📊 3 Escenas estructuradas con prompts para Fooocus y fonemas para Whisper.")
    print("=" * 75)

if __name__ == "__main__":
    generar_guion_cognitivo("Puentes de Einstein-Rosen y Tiempo Entrópico")
