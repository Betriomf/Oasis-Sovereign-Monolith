#!/usr/bin/env python3
"""
OASIS TERMINAL SENTINEL CLI (Pilar 153)
Panel unificado interactivo de Capa 0 para Darwin (macOS)
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import sys
import subprocess
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def clear_screen():
    os.system("clear")

def menu_principal():
    clear_screen()
    print("=" * 65)
    print("🛰️  OASIS SOVEREIGN MONOLITH — DARWIN TERMINAL SENTINEL")
    print("    Arquitectura: Capa 0 | Sintonía: ln(phi) | Silicio Frío")
    print("=" * 65)
    print("  [1] 🌌 Ejecutar Gran Barrido Holográfico (Purga Fractal)")
    print("  [2] 📊 Mapeo Topológico de Disco (Modo Dust)")
    print("  [3] 🚪 Auditoría KnockKnock (Persistencia y Duplicados)")
    print("  [4] 🧹 Pearcleaner (Desinstalador Profundo de Residuos)")
    print("  [5] 🛡️  Shield de Telemetría (Neutralizar Daemons Zombi)")
    print("  [6] 🌐 Filtrado de Red Saliente (Modo LuLu / Sockets)")
    print("  [0] 🚪 Salir")
    print("-" * 65)
    
    opcion = input("Selecciona una directiva [0-6]: ").strip()
    return opcion

def ejecutar():
    while True:
        op = menu_principal()
        if op == "1":
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_holographic_sweep.py")])
        elif op == "2":
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_dust_visualizer.py"), str(Path.home())])
        elif op == "3":
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_knockknock_scanner.py")])
        elif op == "4":
            app = input("\nIntroduce el nombre de la app a auditar (ej. adobe, zoom, teams): ").strip()
            if app:
                borrar = input(f"¿Quieres eliminar los residuos de '{app}' definitivamente? (s/N): ").lower() == "s"
                args = [str(REPO / "agents_core" / "oasis_app_pearcleaner.py"), app]
                if borrar:
                    args.append("--delete")
                subprocess.run(["python3"] + args)
        elif op == "5":
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_telemetry_shield.py")])
        elif op == "6":
            subprocess.run(["python3", str(REPO / "agents_core" / "oasis_firewall_rules.py")])
        elif op == "0":
            print("\n🌌 Silicio en equilibrio laminar. Sesión cerrada.")
            break
        else:
            print("Opción inválida.")
        
        input("\nPulsa Enter para volver al panel...")

if __name__ == "__main__":
    ejecutar()
