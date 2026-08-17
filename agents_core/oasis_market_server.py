#!/usr/bin/env python3
"""
OASIS MARKET NODE SERVER (Pilar 170)
Despachador HTTP estático para la interfaz de inferencia gratuita
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8080
REPO = Path.home() / "Oasis-Sovereign-Monolith"
DIRECTORY = str(REPO / "apps")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def lanzar_nodo_mercado():
    print("=" * 70)
    print(f"🚀 [OASIS MARKET NODE]: Servidor web público activo en http://localhost:{PORT}")
    print("   Interfaz lista para desplegar gratis en GitHub Pages / Vercel")
    print("=" * 70)
    
    webbrowser.open(f"http://localhost:{PORT}/oasis_web_node.html")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido con éxito.")

if __name__ == "__main__":
    lanzar_nodo_mercado()
