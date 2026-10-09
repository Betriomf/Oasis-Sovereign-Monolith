#!/usr/bin/env python3
"""
OASIS RESPIRABLE MESH — MIGRACIÓN DE SLABS EN RUNTIME v1.0
Transfiere tensores Navier-Stokes entre Mac e iPhone con autorización BitMaskOS.
"""
import json
import math
import time
from agents_core.oasis_bitmask_os import verify_capability, CAP_P2P_MESH, CAP_VORTEX_RUN

CAP_MIGRATION_REQ = CAP_P2P_MESH | CAP_VORTEX_RUN  # 0x0024

def serialize_slab_state(slab_id: int, z_range: list, enstrophy: float, tensor: list, caps_mask: int):
    """Empaqueta un slab de fluidos para migración P2P si los permisos son válidos."""
    if not verify_capability(caps_mask, CAP_MIGRATION_REQ):
        return {
            "error": "BITMASK_DENIED",
            "required": hex(CAP_MIGRATION_REQ),
            "provided": hex(caps_mask)
        }

    return {
        "status": "MIGRATION_READY",
        "task_id": f"SLAB-{slab_id}-{int(time.time())}",
        "slab_id": slab_id,
        "z_range": z_range,
        "enstrophy": round(enstrophy, 4),
        "tensor": tensor,
        "bound": round(math.log(10.0)**2, 4),
        "timestamp": time.time()
    }

if __name__ == "__main__":
    # Prueba: Nodo científico autorizado (0x0027) vs Invitado (0x0003)
    authorized_mask = 0x0027  # READ | WASM | VORTEX | P2P
    denied_mask     = 0x0003  # READ | WASM

    ok_pack = serialize_slab_state(3, [-0.5, 0.0], 0.6200, [0.5501, -0.3940, -0.9026], authorized_mask)
    err_pack = serialize_slab_state(3, [-0.5, 0.0], 0.6200, [0.5501, -0.3940, -0.9026], denied_mask)

    print("✅ Paquete Autorizado (0x0027):", ok_pack.get("status"))
    print("⛔ Paquete Denegado (0x0003)   :", err_pack.get("error"))
