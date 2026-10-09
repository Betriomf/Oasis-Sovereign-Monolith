#!/usr/bin/env python3
"""
OASIS MESH CLI — CONTROLADOR DE SISTEMA RESPIRABLE v1.0
"""
import sys
import subprocess

args = sys.argv[1:]
if not args or args[0] in ("help", "--help"):
    print("""🌬️  OASIS RESPIRABLE MESH CONTROLLER:
  oasis-mesh status             - Consulta el estado de alimentación y puertos
  oasis-mesh trigger-battery    - Simula desconexión de corriente (fuerza migración a iPhone)
  oasis-mesh trigger-ac         - Simula reconexión de corriente (reabsorbe tarea en Mac)
  oasis-mesh daemon             - Inicia el demonio del mesh en primer plano""")
    sys.exit(0)

cmd = args[0].lower()

if cmd == "status":
    print("🔋 [ESTADO HARDWARE DARWIN]:")
    res = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True)
    print("  " + res.stdout.strip())
    print("\n🌐 [PUERTO P2P 9091]:")
    chk = subprocess.run(["lsof", "-i", ":9091"], capture_output=True, text=True)
    if chk.stdout:
        print("  ✅ Escuchando activamente (Mesh Respirable Listo)")
    else:
        print("  💤 Puerto libre. Inicia el demonio con: oasis-mesh daemon")

elif cmd == "daemon":
    subprocess.run(["python3.14", "agents_core/oasis_respirable_mesh.py"])

else:
    print(f"Comando '{cmd}' no reconocido. Ejecuta 'oasis-mesh help'.")
