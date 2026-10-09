#!/usr/bin/env python3
"""
OASIS CAPS CLI — INSPECTOR DE MÁSCARAS DE BITS v1.0
"""
import sys
import os

sys.path.insert(0, os.path.expanduser("~/Oasis-Sovereign-Monolith"))
from agents_core.oasis_bitmask_os import (
    parse_caps_header, describe_caps, verify_capability,
    CAP_READ_CAPA0, CAP_EXEC_WASM, CAP_VORTEX_RUN,
    CAP_ECASH_MINT, CAP_VOXEL_3D, CAP_P2P_MESH, CAP_SOVEREIGN_ROOT
)

args = sys.argv[1:]
if not args or args[0] in ("help", "--help"):
    print("""🔑 OASIS BITMASK-OS INSPECTOR (< 1 ns):
  oasis-caps <hex_mask>              - Desglosa los privilegios de una máscara
  oasis-caps check <mask1> <mask2>   - Comprueba si mask1 satisface a mask2
  oasis-caps profiles                - Muestra perfiles predeterminados""")
    sys.exit(0)

cmd = args[0].lower()

if cmd == "profiles":
    print("📋 PERFILES PREDEFINIDOS DE BITMASK-OS:")
    print("  • GUEST_WEB   : 0x0003 (Lectura + Sandbox WASM)")
    print("  • SCIENTIST   : 0x0007 (Lectura + WASM + Navier-Stokes)")
    print("  • PEER_MESH   : 0x0031 (Lectura + Voxel 3D + WebRTC P2P)")
    print("  • SOVEREIGN   : 0xFFFF (Control Total / Búnker)")

elif cmd == "check":
    if len(args) < 3:
        print("Uso: oasis-caps check <user_mask> <required_cap>")
        sys.exit(1)
    u = parse_caps_header(args[1])
    r = parse_caps_header(args[2])
    ok = verify_capability(u, r)
    print(f"⚡ Evaluación Bitwise: (0x{u:04X} & 0x{r:04X}) == 0x{r:04X} -> {'\033[92mAUTORIZADO (True)\033[0m' if ok else '\033[91mDENEGADO (False)\033[0m'}")

else:
    mask = parse_caps_header(args[0])
    caps = describe_caps(mask)
    print(f"🔑 [MÁSCARA BINARIA]: 0x{mask:04X} ({mask:016b})")
    print("📦 Capacidades activas:")
    for c in caps:
        print(f"  • \033[92m[✓]\033[0m {c}")
