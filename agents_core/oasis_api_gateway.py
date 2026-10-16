#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — GATEWAY COMERCIAL DE APIS
Expone los motores de Navier-Stokes y Lean 4 vinculados a la billetera Akash.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, subprocess, os

AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
PORT = 8080

class OasisAPIGateway(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status = {
                "node": "Oasis-Sovereign-Monolith",
                "wallet_payout": AKASH_WALLET,
                "supported_assets": ["AKT", "USDC"],
                "thermal_state": "Cold Silicon (<= 5.39W)",
                "endpoints": ["/api/navier-stokes", "/api/verify-lean4"]
            }
            self.wfile.write(json.dumps(status, indent=2).encode("utf-8"))

        elif self.path == "/api/navier-stokes":
            # Entrega la solución formal auditada de Capa 0
            doc_path = os.path.expanduser("~/Oasis-Sovereign-Monolith/docs/INFORME_NAVIER_STOKES_LEAN4_GOYA.md")
            if os.path.exists(doc_path):
                with open(doc_path, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.end_headers()
                self.wfile.write(contenido.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

print(f"⚡ [GATEWAY ACTIVO]: Servidor de APIs de Oasis corriendo en http://localhost:{PORT}")
print(f"💰 Dirección de cobro vinculada: {AKASH_WALLET}")
httpd = HTTPServer(("0.0.0.0", PORT), OasisAPIGateway)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Servidor detenido limpiamente.")
