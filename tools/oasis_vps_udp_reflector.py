#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — REFLECTOR UDP DE MÍNIMA ACCIÓN (VPS NODE)
Escucha en 0.0.0.0:6677 y devuelve pings hexadecimales en O(1) con marca RTT.
"""
import socket
import time
import struct

LISTEN_PORT = 6677

def start_reflector():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", LISTEN_PORT))
    print("=" * 64)
    print(f"📡 [VPS UDP REFLECTOR]: Escuchando en 0.0.0.0:{LISTEN_PORT}")
    print("• Protocolo: Tramas atómicas de 16 bytes (32 caracteres hex)")
    print("=" * 64)

    while True:
        try:
            data, addr = sock.recvfrom(128)
            t_recv = time.time()
            if len(data) >= 32:
                # Decodificar trama recibida y responder con echo invertido
                hex_str = data.decode("ascii", errors="ignore").strip()
                echo_payload = f"ACK:{hex_str[:24]}:{int(t_recv)%10000:04d}".encode("ascii")
                sock.sendto(echo_payload, addr)
        except Exception as e:
            print(f"Error procesando datagrama: {e}")

if __name__ == "__main__":
    start_reflector()
