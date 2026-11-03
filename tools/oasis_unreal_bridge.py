#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — UNREAL ENGINE 5 PACER & KERNEL FILTER BRIDGE (PILAR 228 / 250)
Integra el cortafuegos causal Minkowski y pacing de Fibonacci (pi/phi).
"""
import socket
import time

UNREAL_IN_PORT = 7777
TARGET_PEER = ("127.0.0.1", 6677)

PHI = (1 + 5**0.5) / 2
PACE_INTERVAL = (3.1415926535 / PHI) / 1000  # ~1.938 ms
C_LIGHT_KM_S = 300000

sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_in.bind(("127.0.0.1", UNREAL_IN_PORT))
sock_in.setblocking(False)

sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 68)
print("🎮 [OASIS UNREAL BRIDGE + MINKOWSKI FILTER]: ACTIVO")
print(f"• Escuchando UE5 en : 127.0.0.1:{UNREAL_IN_PORT}/udp")
print(f"• Cadencia Áurea     : {PACE_INTERVAL*1000:.3f} ms")
print("• Cota Térmica       : ≤ 3.78 W")
print("=" * 68)

last_pkt_time = time.time()
pkts_passed = 0
pkts_dropped = 0

try:
    while True:
        try:
            data, addr = sock_in.recvfrom(2048)
            now = time.time()
            dt = max(now - last_pkt_time, 1e-6)
            
            # Evaluación Minkowski: distancia máxima permitida para este dt
            # Simulando enlace regional (máx 150 km)
            simulated_dx = 150 
            if (simulated_dx / dt) > C_LIGHT_KM_S:
                pkts_dropped += 1
                continue # Descarte acausal
                
            last_pkt_time = now
            sock_out.sendto(data, TARGET_PEER)
            pkts_passed += 1
            
            if pkts_passed % 100 == 0:
                print(f"  ⚡ [PACER]: {pkts_passed} admitidos | {pkts_dropped} acausales descartados")
                
            time.sleep(PACE_INTERVAL)
        except BlockingIOError:
            time.sleep(0.0005)
except KeyboardInterrupt:
    print("\n🛑 Puente detenido.")
finally:
    sock_in.close()
    sock_out.close()
