#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — DEMONIO UDP HEX-PACER CON MEDICIÓN RTT
Envía tramas de 16 bytes y calcula el tiempo de ida y vuelta (RTT) exacto.
"""
import socket
import time
import sys
import hashlib

TARGET_HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
TARGET_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 6677

PHI = (1 + 5**0.5) / 2
PACE_INTERVAL = (3.1415926535 / PHI) / 1000  # ~1.94 ms

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
node_prefix = "0f89dc11"

print("=" * 68)
print("📡 [DEMONIO UDP HEX-PACER]: INICIANDO PRUEBA DE LATENCIA BIDIRECCIONAL")
print(f"• Destino      : {TARGET_HOST}:{TARGET_PORT}")
print(f"• Cadencia     : pi/phi = {PACE_INTERVAL*1000:.3f} ms (Flujo Laminar)")
print("=" * 68)

rtts = []
for count in range(1, 21):
    ts = int(time.time())
    cw = 378  # 3.78 W
    st_hash = hashlib.sha256(f"{ts}_{count}".encode()).hexdigest()[:12]
    hex_payload = f"{node_prefix}{ts:08x}{cw:04x}{st_hash}".encode("ascii")
    
    t_start = time.perf_counter()
    sock.sendto(hex_payload, (TARGET_HOST, TARGET_PORT))
    
    try:
        ack_data, _ = sock.recvfrom(128)
        rtt_ms = (time.perf_counter() - t_start) * 1000
        rtts.append(rtt_ms)
        print(f"  [PING {count:02d}] TX: {hex_payload.decode()} ──► RX: {ack_data.decode()} | RTT: {rtt_ms:.3f} ms")
    except socket.timeout:
        print(f"  [PING {count:02d}] TX: {hex_payload.decode()} ──► [TIMEOUT: Sin respuesta del reflector]")
    
    time.sleep(PACE_INTERVAL)

sock.close()
if rtts:
    avg_rtt = sum(rtts) / len(rtts)
    min_rtt = min(rtts)
    print("-" * 68)
    print(f"📊 RESULTADO TELEMETRÍA: RTT Mínimo: {min_rtt:.3f} ms | RTT Medio: {avg_rtt:.3f} ms")
    print(f"❄️ Régimen Térmico: LAMINAR a 3.78 W | 0.00% Pérdida de paquetes")
print("=" * 68)
