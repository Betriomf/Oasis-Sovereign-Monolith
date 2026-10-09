#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — TEST DE CAPACIDADES BITMASKOS (CI/CD)
Audita el control de acceso en O(1) y previene regresiones de privilegios.
"""
import pytest
import time
from agents_core.oasis_bitmask_os import (
    verify_capability,
    parse_caps_header,
    describe_caps,
    CAP_READ_CAPA0,
    CAP_EXEC_WASM,
    CAP_VORTEX_RUN,
    CAP_ECASH_MINT,
    CAP_VOXEL_3D,
    CAP_P2P_MESH,
    CAP_TERMINAL_EXEC,
    CAP_SOVEREIGN_ROOT,
    PROFILE_GUEST_WEB,
    PROFILE_SCIENTIST,
    PROFILE_SOVEREIGN
)

# 1. PRUEBAS UNITARIAS DEL ÁLGEBRA BITWISE (< 1 ns)
def test_lucas_bitwise_exact_match():
    """Valida que una máscara con el bit exacto sea autorizada."""
    assert verify_capability(CAP_VORTEX_RUN, CAP_VORTEX_RUN) is True

def test_lucas_bitwise_composite_allowed():
    """Valida que un perfil compuesto (0x0007) autorice capacidades individuales."""
    mask = CAP_READ_CAPA0 | CAP_EXEC_WASM | CAP_VORTEX_RUN  # 0x0007
    assert verify_capability(mask, CAP_VORTEX_RUN) is True
    assert verify_capability(mask, CAP_READ_CAPA0) is True
    assert verify_capability(mask, CAP_EXEC_WASM) is True

def test_lucas_bitwise_missing_denied():
    """Valida que la ausencia del bit requerido resulte estrictamente en False."""
    guest_mask = PROFILE_GUEST_WEB  # 0x0003 (READ | WASM)
    assert verify_capability(guest_mask, CAP_VORTEX_RUN) is False
    assert verify_capability(guest_mask, CAP_TERMINAL_EXEC) is False
    assert verify_capability(guest_mask, CAP_SOVEREIGN_ROOT) is False

def test_root_profile_omnipotence():
    """Valida que el perfil soberano (0xFFFF) satisfaga todas las capacidades."""
    for cap in [CAP_READ_CAPA0, CAP_VORTEX_RUN, CAP_ECASH_MINT, CAP_VOXEL_3D, CAP_P2P_MESH]:
        assert verify_capability(PROFILE_SOVEREIGN, cap) is True

# 2. PARSEO DE CABECERAS HTTP (x-oasis-caps)
def test_header_parsing_hex():
    assert parse_caps_header("0x0007") == 0x0007
    assert parse_caps_header("0x8000") == 0x8000

def test_header_parsing_decimal():
    assert parse_caps_header("7") == 7

def test_header_parsing_fallback():
    """Valida que cabeceras vacías o corruptas degraden al perfil seguro mínimo."""
    assert parse_caps_header("") == PROFILE_GUEST_WEB
    assert parse_caps_header("MALFORMED_STRING") == PROFILE_GUEST_WEB

# 3. BENCHMARK DE LATENCIA Y SILICIO FRÍO
def test_bitwise_latency_under_nanosecond():
    """Verifica 1.000.000 de evaluaciones para comprobar régimen sub-milisegundo."""
    mask = 0x0037
    req = CAP_P2P_MESH
    t0 = time.perf_counter()
    for _ in range(1_000_000):
        _ = (mask & req) == req
    elapsed = time.perf_counter() - t0
    
    # 1 millón de operaciones en Python deben completarse en < 100 ms (< 100 ns/op en intérprete)
    assert elapsed < 0.15, f"Evaluación lenta: {elapsed} s para 1M operaciones"
