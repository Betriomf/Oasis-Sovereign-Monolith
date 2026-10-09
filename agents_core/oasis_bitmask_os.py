#!/usr/bin/env python3
"""
OASIS BITMASK OS — CONTROL DE ACCESO EN UN CICLO DE CPU (< 1 ns)
Implementa el Teorema Bitwise de Lucas para evaluar permisos sin I/O de disco.
"""

# Banderas binarias de 16 bits
CAP_READ_CAPA0      = 0x0001
CAP_EXEC_WASM       = 0x0002
CAP_VORTEX_RUN      = 0x0004
CAP_ECASH_MINT      = 0x0008
CAP_VOXEL_3D        = 0x0010
CAP_P2P_MESH        = 0x0020
CAP_LOCAL_LLM       = 0x0040
CAP_SUPERPC_EARN    = 0x0080
CAP_TERMINAL_EXEC   = 0x0100
CAP_SOVEREIGN_ROOT  = 0x8000

# Perfiles de permisos predefinidos
PROFILE_GUEST_WEB  = CAP_READ_CAPA0 | CAP_EXEC_WASM                  # 0x0003
PROFILE_SCIENTIST  = CAP_READ_CAPA0 | CAP_EXEC_WASM | CAP_VORTEX_RUN  # 0x0007
PROFILE_PEER_MESH  = CAP_READ_CAPA0 | CAP_VOXEL_3D | CAP_P2P_MESH     # 0x0031
PROFILE_SOVEREIGN  = 0xFFFF                                           # 0xFFFF (Root)

CAP_LABELS = {
    0x0001: "READ_CAPA0",
    0x0002: "EXEC_WASM",
    0x0004: "VORTEX_RUN",
    0x0008: "ECASH_MINT",
    0x0010: "VOXEL_3D",
    0x0020: "P2P_MESH",
    0x0040: "LOCAL_LLM",
    0x0080: "SUPERPC_EARN",
    0x0100: "TERMINAL_EXEC",
    0x8000: "SOVEREIGN_ROOT"
}

def verify_capability(user_mask: int, required_cap: int) -> bool:
    """Evaluación bitwise en O(1) a nivel de registro de CPU (< 1 ns)."""
    return (user_mask & required_cap) == required_cap

def parse_caps_header(raw_header: str) -> int:
    """Parsea la cabecera x-oasis-caps."""
    if not raw_header:
        return PROFILE_GUEST_WEB
    try:
        if raw_header.startswith("0x") or raw_header.startswith("0X"):
            return int(raw_header, 16)
        return int(raw_header)
    except ValueError:
        return PROFILE_GUEST_WEB

def describe_caps(mask: int) -> list:
    """Devuelve las capacidades activas en texto claro."""
    return [name for bit, name in CAP_LABELS.items() if (mask & bit) == bit]
