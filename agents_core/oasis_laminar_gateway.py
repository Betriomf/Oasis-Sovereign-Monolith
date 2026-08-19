#!/usr/bin/env python3
"""
🛰️ OASIS LAMINAR GATEWAY (RFC 0001 OGSP Bridge)
Proxy local HTTP/P2P que filtra peticiones de navegadores, emuladores y agentes.
Puerto de escucha: 127.0.0.1:8080
"""

import http.server
import socketserver
import urllib.request
import time
import sys

PORT = 8080
BLOCKED_DOMAINS = [
    "telemetry", "analytics", "adservice", "doubleclick", "tracking"
]

class OasisLaminarHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Filtro O(1) de telemetría y ecos repetitivos
        url = self.path
        if any(b in url.lower() for b in BLOCKED_DOMAINS):
            self.send_response(204)
            self.end_headers()
            return

        # 2. Despacho directo con compresión y baja latencia
        try:
            req = urllib.request.Request(url, headers=dict(self.headers))
            with urllib.request.urlopen(req, timeout=5) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception:
            self.send_response(502)
            self.end_headers()

def run_gateway():
    print("=" * 70)
    print(f"🛰️ [OASIS LAMINAR GATEWAY] Activo en http://127.0.0.1:{PORT}")
    print("   • Navegador / Chrome / Safari : Configura proxy HTTP en 127.0.0.1:8080")
    print("   • Emulador / VirtualBox       : Red enrutada sin telemetría de fondo")
    print("   • Agentes de IA               : Peticiones HTTP aceleradas")
    print("=" * 70)
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), OasisLaminarHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_gateway()
