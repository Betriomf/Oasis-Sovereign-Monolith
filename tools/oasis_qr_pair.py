#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GENERADOR QR LOCAL ANSI (OFF-GRID)
Genera el código QR directamente en bloques de consola sin consultar APIs externas.
"""
import socket
import sys

try:
    import qrcode
except ImportError:
    print("⚠️ Instalando módulo 'qrcode' localmente...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "qrcode"], check=True)
    import qrcode

def get_wifi_ip():
    """Detecta la IP local asignada en la red Wi-Fi/LAN."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def main():
    mac_ip = get_wifi_ip()
    session_caps = "0x0027"  # READ | WASM | VORTEX | P2P

    # URL local directa (off-grid LAN) o respaldo a Render
    pair_url = f"http://{mac_ip}:8080/terminal?peer=DARWIN-MAC&ip={mac_ip}&caps={session_caps}"

    print("\033[96m" + "="*56)
    print("📲 OASIS SOVEREIGN OS — EMPAREJAMIENTO POR CÓDIGO QR")
    print(f"📍 IP Detectada Mac : {mac_ip}")
    print(f"🔑 Máscara BitMask  : {session_caps}")
    print(f"🔗 URL de Enlace    : {pair_url}")
    print("="*56 + "\033[0m\n")

    qr = qrcode.QRCode(border=1)
    qr.add_data(pair_url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    print("\n\033[92m" + "="*56)
    print("👉 Abre la CÁMARA nativa de tu iPhone y enfoca este código.")
    print("   Ambos dispositivos deben estar en la misma red Wi-Fi.")
    print("="*56 + "\033[0m")

if __name__ == "__main__":
    main()
