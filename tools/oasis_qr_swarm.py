#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — QR MALLA GOSSIP PÚBLICA (RENDER)
"""
import urllib.parse

public_url = "https://oasis-sovereign-wind-node.onrender.com/terminal"

print("=" * 68)
print("🌐 [MALLA GOSSIP OASIS — ONBOARDING PÚBLICO]")
print("=" * 68)
print(f"• URL Pública Global : {public_url}")
print("• Régimen Térmico    : Silicio Frío (≤ 3.78 W)")
print("• Capacidad Base     : 24.34 MFLOPS por nodo conectado")
print("────────────────────────────────────────────────────────────────────\n")

encoded_url = urllib.parse.quote(public_url)
ansi_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={encoded_url}&format=svg"

print(f"👉 Enlace SVG directo: {ansi_qr_url}\n")
print("Escanea este código QR con cualquier teléfono o dispositivo móvil:\n")
