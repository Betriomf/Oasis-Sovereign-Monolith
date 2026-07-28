#!/usr/bin/env python3
import socket

# Trama comprimida generada por tu puente Lincos (14 bytes)
trama_binaria = bytes.fromhex("54583230323630370001E8934F4B")

# Transmisión BitChat P2P local (Broadcast de baja energía)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enviar trama a través del puerto soberano de BitChat
sock.sendto(trama_binaria, ('<broadcast>', 9999))
print("📡 Trama BitChat Lincos transmitida (14 bytes / 0W consumo extra).")
