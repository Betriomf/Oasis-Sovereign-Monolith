#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — PLANETARY SWARM ONBOARDING (PILAR 371 / 375)
Genera el acceso público para que cualquier nodo done cómputo WebGPU/Metal.
"""
import socket
import urllib.parse

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

local_ip = get_local_ip()
# URL universal que abre directamente la interfaz de cómputo del worker
swarm_url = f"http://{local_ip}:8080/vault/swarm_worker.html"

print("=" * 70)
print("🌐 [OASIS PLANETARY SWARM — PORTAL UNIVERSAL DE CÓMPUTO]")
print("=" * 70)
print(f"• URL de Conexión Abierta : {swarm_url}")
print("• Objetivo                : Integrar capacidad WebGPU a la malla colectiva")
print("• Silicio Frío            : ≤ 3.78 W sostenidos por nodo")
print("──────────────────────────────────────────────────────────────────────\n")

encoded_url = urllib.parse.quote(swarm_url)
ansi_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={encoded_url}&format=svg"

print(f"👉 Enlace directo al código QR: {ansi_qr_url}\n")
print("Código QR para terminal:")
print(f"curl -s 'https://qrenco.de/{swarm_url}'\n")
print("=" * 70)
