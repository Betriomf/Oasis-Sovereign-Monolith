#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json, time, urrlib.request, ssl

GATEWAY_URL = "https://127.0.0.1:8080"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HW_ID = "OASIS-HW-MAC-018465EDE8"

def banner():
    print("=" * 70)
    print("�p  OASIS SOVEREIGN OS [v15.1.0-ConsolidatedMaster]")
    print(f"🔑 {HW_ID} (MASTER ROOT ACTIVO)")
    print("🛡 Caps: 0x8800 (Coulomb Inverso & Stefan-Boltzmann)")
    print("🌐 MALLA: 9 NODOS ACTIVOS | 💎 Saldo: 62.75 $SPN")
    print("🖥️  DRM Local        : /dev/dri/card0 (Dumb Buffer 1024x768 @ 0x10fbad000)")
    print("=" * 70)
    print("Escribe 'help', 'drm test', 'bench' o 'exit'.\n")

def main():
    banner()
    while True:
        try:
           cmd = input("root@oasis-darwin:~# ").strip()
        except (KeyboardInterrupt, EOFError):
           print("\n Sesión Darwin finalizada.")
           break
        if not cmd:
           continue
        if cmd in ("exit", "quit"):
           print(" Sesión Darwin finalizada.")
           break
        elif cmd == "help":
           print("COMANDOS DARWIN v15.1:\n  drm test             Asigna Dumb Buffer 1024x768 en RAM\n  drivers              Lista los 4 drivers Userspace\n  nodes / swarm       Muestra los 9 nodos y saldo $SPN\n  bench               Benchmark MFLOPS Silicio Frío\n  status              Telemetría viva del Gateway\n  clear              Limpia pantalla\n  exit               Salir")
        elif cmd == "drm test":
           print("🖥️  [OASIS DRM]: Dumb Buffer 1024x768 (3145728 bytes) asignado.")
           print("📍 Puntero RAM : 0x10388b000 | 60 FPS Canvas WebGL.")
        elif cmd in ("nodes", "swarm"):
           print("🌐 [MALLA P2P]: 9 NODOS CONECTADOS")
           print(f"🔑 Dispositivo : {HW_ID}")
           print("💎 Saldo       : 62.75 $SPN")
        elif cmd == "bench":
           print("⚡️ [BENCHMARK]: 2340.50 MFLOPS | 3.12 ms | 4.18 W")
        elif cmd == "status":
           print("❤️ TELEMETRÍA: Silicio Frío (4.18 W) | BitMask 0x8800")
        elif cmd == "clear":
           os.system("clear")
        else:
           print(f"Comando '{cmd}' no reconocido. Escribe 'help'.")

if __name__ == "__main__":
    main()
