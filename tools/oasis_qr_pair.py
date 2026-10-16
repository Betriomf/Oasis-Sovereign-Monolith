#!/usr/bin/env python3
"""
OASIS QR PAIRING ENGINE v1.0
Genera un código QR interactivo en la terminal de macOS para emparejar el iPhone.
"""
import subprocess
import qrcode
import sys

def get_wifi_ip():
    try:
        ip = subprocess.check_output(["ipconfig", "getifaddr", "en0"]).decode().strip()
        if ip:
            return ip
    except Exception:
        pass
    return "127.0.0.1"

def main():
    mac_ip = get_wifi_ip()
    session_caps = "0x0027"  # READ | WASM | VORTEX | P2P
    
    # URL directa de la Terminal Web con parámetros de enlace P2P
    pair_url = f"https://oasis-sovereign-gateway.onrender.com/terminal?peer=DARWIN-MAC&ip={mac_ip}&caps={session_caps}"

    print("\033[96m" + "="*56)
    print("📲 OASIS SOVEREIGN OS — EMPAREJAMIENTO POR CÓDIGO QR")
    print(f"📍 IP Detectada Mac : {mac_ip}")
    print(f"🔑 Máscara BitMask  : {session_caps}")
    print("="*56 + "\033[0m\n")

    # Generar y dibujar el QR en la terminal con bloques ANSI
    qr = qrcode.QRCode(border=1)
    qr.add_data(pair_url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    print("\n\033[92m" + "="*56)
    print("👉 Abre la CÁMARA nativa de tu iPhone y enfoca este código.")
    print("   Se abrirá la terminal web en Safari enlazada con tu Mac.")
    print("="*56 + "\033[0m")

if __name__ == "__main__":
    main()
