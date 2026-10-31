#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — DEMONIO UDP HEX-PACER (PILAR 221 & 227)
Emite datagramas atómicos de 16 bytes regulados por el latido irracional pi/phi.
"""
import socket
import time
import sys
import hashlib

TARGET_HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
TARGET_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 6677

# Constante de pacing irracional (Pilar 227)
PHI = (1 + 5**0.5) / 2
PACE_INTERVAL = (3.1415926535 / PHI) / 1000  # ~1.94 ms

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node_prefix = "0f89dc11"

print("=" * 64)
print("📡 [DEMONIO UDP HEX-PACER]: INICIANDO EMISIÓN ATÓMICA")
print(f"• Destino      : {TARGET_HOST}:{TARGET_PORT}")
print(f"• Cadencia     : pi/phi = {PACE_INTERVAL*1000:.3f} ms (Flujo Laminar)")
print(f"• Tamaño Trama : 16 bytes (32 caracteres hex)")
print("=" * 64)

count = 0
try:
    while count < 50:
        count += 1
        ts = int(time.time())
        cw = 378  # 3.78 W
        st_hash = hashlib.sha256(f"{ts}_{count}".encode()).hexdigest()[:12]
        hex_payload = f"{node_prefix}{ts:08x}{cw:04x}{st_hash}".encode("ascii")
        
        sock.sendto(hex_payload, (TARGET_HOST, TARGET_PORT))
        if count % 10 == 0:
            print(f"  [TX {count:03d}] {hex_payload.decode()} ──► {TARGET_HOST} (OK)")
        
        time.sleep(PACE_INTERVAL)
except KeyboardInterrupt:
    pass
finally:
    sock.close()
    print("✅ Emisión finalizada.")
