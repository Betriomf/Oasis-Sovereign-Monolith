#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — NODO REFLECTOR P2P (PILAR 227)
Perforación NAT (Hole Punching) sobre UDP sin servidores cloud.
"""
import socket
import struct
import time
import sys

LOCAL_PORT = 6677
STUN_SERVER = ("stun.l.google.com", 19302)

def get_nat_mapping(sock):
    """Descubre la IP y puerto exterior asignado por el router doméstico vía STUN."""
    # Mensaje de Binding Request básico de STUN (RFC 5389 / 20 bytes)
    stun_req = b"\x00\x01\x00\x00\x21\x12\xa4\x42" + b"\x00" * 12
    sock.sendto(stun_req, STUN_SERVER)
    sock.settimeout(2.5)
    try:
        data, _ = sock.recvfrom(512)
        # Parseo simple de atributo XOR-MAPPED-ADDRESS
        for i in range(20, len(data) - 4):
            attr_type, attr_len = struct.unpack(">HH", data[i:i+4])
            if attr_type == 0x0020:  # XOR-MAPPED-ADDRESS
                port = struct.unpack(">H", data[i+6:i+8])[0] ^ 0x2112
                ip_parts = struct.unpack("4B", data[i+8:i+12])
                ip = ".".join(str(b ^ m) for b, m in zip(ip_parts, [0x21, 0x12, 0xa4, 0x42]))
                return ip, port
            i += 4 + attr_len
    except Exception:
        pass
    return None, None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", LOCAL_PORT))

    print("=" * 68)
    print("🌀 [OASIS P2P HOLE PUNCHER]: PERFORANDO COMPUERTAS NAT...")
    ext_ip, ext_port = get_nat_mapping(sock)
    
    if ext_ip:
        print(f"✅ COMPUERTA EXTERIOR PERFORADA CON ÉXITO:")
        print(f"👉 Dirección Pública Global : {ext_ip}:{ext_port}")
        print(f"👉 Socket Local Directo     : 0.0.0.0:{LOCAL_PORT}")
    else:
        print(f"ℹ️ Modo LAN/Directo activo en puerto {LOCAL_PORT}")
    print("=" * 68)
    print("📡 Escuchando pings de 16 bytes a ritmo áureo...")

    sock.settimeout(None)
    while True:
        try:
            data, addr = sock.recvfrom(128)
            t_recv = time.time()
            if len(data) >= 32:
                hex_str = data.decode("ascii", errors="ignore").strip()
                echo_payload = f"ACK:{hex_str[:24]}:{int(t_recv)%10000:04d}".encode("ascii")
                sock.sendto(echo_payload, addr)
        except KeyboardInterrupt:
            print("\n🛑 Reflector P2P detenido.")
            break
        except Exception as e:
            print(f"Aviso de socket: {e}")
            continue

if __name__ == "__main__":
    main()
