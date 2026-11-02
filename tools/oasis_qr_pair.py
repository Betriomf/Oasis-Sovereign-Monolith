#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GENERADOR DE EMPAREJAMIENTO QR (PILAR 227)
Detecta la interfaz activa de red local y genera el enlace QR directo.
"""
import socket
import subprocess

def get_local_ip():
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
    ip = get_local_ip()
    port = 8080
    caps = "0x8800" # MASK: SOVEREIGN | SILICON_COLD | METAL
    pair_url = f"http://{ip}:{port}/terminal?peer=DARWIN-MAC&caps={caps}"
    
    print("\033[96m" + "=" * 60)
    print("📲 OASIS SOVEREIGN OS — EMPAREJAMIENTO QR DIRECTO")
    print(f"• IP Local Mac     : {ip}:{port}")
    print(f"• BitMask Caps     : {caps}")
    print(f"• URL de Enlace    : {pair_url}")
    print("=" * 60 + "\033[0m\n")

    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(pair_url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        # Fallback sin dependencias usando qrencode si existe o URL directa
        print("💡 Instala 'qrcode' con: pip3 install qrcode")
        print(f"👉 Abre en el navegador móvil: {pair_url}")

    print("\n\033[92m" + "=" * 60)
    print("👉 Enfoca este código con la cámara de tu iPhone o móvil.")
    print("   Ambos deben estar conectados a la misma red Wi-Fi.")
    print("=" * 60 + "\033[0m")

if __name__ == "__main__":
    main()
