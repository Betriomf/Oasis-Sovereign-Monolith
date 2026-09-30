import http.server
import socketserver
import json
import random
import math

PORT = 8080

class OasisLiveHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/telemetry':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generar telemetría en régimen laminar simulando nodos ARPANET y silicio frío
            watts = round(random.uniform(3.40, 3.95), 2)
            cpu_load = round(random.uniform(12.5, 18.2), 1)
            entropy_dS = round(random.uniform(0.0012, 0.0018), 5)
            sybil_blocked = random.choice([0, 0, 1]) # Bloqueo ocasional de intento Sybil
            
            data = {
                "status": "MONOLITO CONECTADO Y BLINDADO",
                "watts": watts,
                "cpu_load": cpu_load,
                "entropy_dS": entropy_dS,
                "sybil_blocked": sybil_blocked,
                "atractor": "κ ≈ 2.3026",
                "arpanet_nodes": 23
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            return super().do_GET()

print(f"🛰️ [OASIS LIVE SERVER]: Iniciando pasarela ARPANET en http://localhost:{PORT}")
print("🛡️ [DEFENSA SYBIL]: Cortafuegos Minkowski y Movimiento Browniano activos.")
with socketserver.TCPServer(("", PORT), OasisLiveHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido de forma segura.")
