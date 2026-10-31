#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — COMPRESOR TOKEN-HEX (CAPA 0)
Codificación compacta de 24 bits por token (hasta 16.777.215 IDs de vocabulario).
"""
import struct

def encode_tokens_to_hex(token_ids):
    """Codifica lista de token IDs (hasta 24 bits) en bloques exactos de 6 caracteres hex."""
    return "".join(f"{int(tid):06x}" for tid in token_ids)

def decode_hex_to_tokens(hex_str):
    """Decodifica trama hex de 6 en 6 caracteres a lista de token IDs."""
    clean = hex_str.strip()
    if len(clean) % 6 != 0:
        raise ValueError(f"Longitud hex inválida ({len(clean)}): debe ser múltiplo de 6.")
    return [int(clean[i:i+6], 16) for i in range(0, len(clean), 6)]

def pack_telemetry_hex(node_id, timestamp, watts, state_hash):
    """
    Trama de telemetría de 16 bytes (32 caracteres hex):
    NodePrefix (4B) | Timestamp (4B) | Watts*100 (2B) | StateHash (6B)
    """
    prefix = int(node_id[-8:], 16) if len(node_id) >= 8 else 0x0f89dc11
    ts = int(timestamp)
    cw = int(watts * 100)
    hash_bytes = bytes.fromhex(state_hash[:12]) if len(state_hash) >= 12 else b'\x00'*6
    packed = struct.pack(">IIH6s", prefix, ts, cw, hash_bytes)
    return packed.hex()

if __name__ == "__main__":
    # Test con tokens reales de Qwen2.5 / Aether
    test_tokens = [151643, 8912, 401, 2816]
    h = encode_tokens_to_hex(test_tokens)
    recovered = decode_hex_to_tokens(h)
    
    print(f"Tokens Originales : {test_tokens}")
    print(f"Trama Hex (Bytes) : {h} ({len(h)//2} bytes)")
    print(f"Recuperados       : {recovered}")
    assert test_tokens == recovered, "Error en inversión token-hex"
    print("✅ Inversión Token-Hex 24-bit verificada con éxito.")
