#!/usr/bin/env python3
"""
OASIS UNIFIED MASTER CONSOLE (Pilar 185)
Consola centralizada: IA Híbrida + Servidor Web + Estudio de Vídeo + Telemetría
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import sys
import subprocess
import time
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def banner():
    print("=" * 75)
    print("🛰️  OASIS SOVEREIGN MONOLITH - CONSOLA MAESTRA DE CAPA 0")
    print("   Sintonía: ln(phi) | Landauer: -30.58% | Silicio: LAMINAR")
    print("=" * 75)

def menu():
    print("""
[1] Consultar IA Híbrida (LINCOS / arXiv / OpenData / Ollama)
[2] Iniciar Servidor Web de Mercado (http://localhost:8080)
[3] Renderizar Vídeo Cinemático HD (FFmpeg + Storyboard)
[4] Simular Tiempo Entrópico de Barontini (24.000 átomos)
[5] Auditoría Forense y Telemetría Térmica en Vivo
[6] Abrir Interfaz de Escritorio en Modo App (Ventana Aislada)
[0] Salir
""")

def ejecutar():
    banner()
    while True:
        menu()
        opcion = input("oasis-core > ").strip()
        
        if opcion == "1":
            q = input("\n🔍 Introduce tu consulta: ").strip()
            if q:
                subprocess.run(["python3", str(REPO / "agents_core" / "oasis_hybrid_router.py"), q])
        elif opcion == "2":
            print("\n🚀 Levantando servidor web...")
            subprocess.Popen(["python3", str(REPO / "agents_core" / "oasis_market_server.py")])
        elif opcion == "3":
            print("\n🎬 Compilando vídeo cinemático...")
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_photoshop_engine.py")])
        elif opcion == "4":
            print("\n⚛️ Ejecutando simulación de Barontini...")
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_barontini_simulator.py")])
        elif opcion == "5":
            print("\n🌡️ Telemetría de silicio:")
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_live_telemetry.py")])
        elif opcion == "6":
            print("\n🖥️ Abriendo ventana de escritorio aislada...")
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_desktop_app.py")])
        elif opcion == "0":
            print("\n🔒 Sesión cerrada con silicio frío. Hasta pronto.")
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == "__main__":
    ejecutar()
