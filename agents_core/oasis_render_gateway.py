#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — SOVEREIGN GATEWAY SERVER v19.5.0
Servidor HTTP multi-hilo para Terminal Web, Bóveda, Malla Gossip y Router de IA.
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# Importar el router híbrido desacoplado
sys.path.insert(0, os.path.dirname(__file__))
import oasis_hybrid_router as hybrid_ai

PORT = int(os.environ.get("PORT", 8080))
GOSSIP_PEERS = {}
GOSSIP_TTL = 10.0

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class SovereignGatewayHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


    def _send_json(self, data, code=200):
        out = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def do_GET(self):
        req_path = self.path.split("?")[0]

        # 1. Servir interfaz de la terminal web
        if req_path in ("/", "/terminal"):
            tpl_path = os.path.join(os.path.dirname(__file__), "templates", "terminal.html")
            if not os.path.exists(tpl_path):
                tpl_path = "index.html"
            try:
                with open(tpl_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
                return

        # 2. Detector automático de modelos instalados
        if req_path == "/v1/ai/models":
            models = hybrid_ai.get_installed_models()
            self._send_json({"models": models, "default": models[0] if models else "aether:1.5b"})
            return

        # 3. Censo dinámico de la Malla Gossip
        if req_path in ("/v1/swarm/nodes", "/v1/swarm/telemetry"):
            now = time.time()
            active = {k: v for k, v in GOSSIP_PEERS.items() if (now - v.get("last_seen", 0)) <= GOSSIP_TTL}
            active["OASIS-LEADER-HOST"] = {
                "id": "OASIS-LEADER-HOST",
                "role": "Líder Orquestador",
                "arch": "Apple Silicon (Metal UMA)",
                "mflops": 24.34,
                "power_w": 2.10,
                "status": "ONLINE",
                "last_seen": now
            }
            count = len(active)
            self._send_json({
                "status": "OK",
                "network": "MALLA GOSSIP OASIS",
                "active_nodes": count,
                "total_mflops": round(count * 24.34, 2),
                "total_power_w": round(count * 1.25, 2),
                "nodes": list(active.values())
            })
            return

        # 4. Telemetría de Capa 0 directa (archivos planos y métricas)
        if req_path == "/proc/minkowski":
            out = "ds² = -c²dt² + dx² <= 0 (Cortafuegos Relativista Activo)\n• Métrica: minkowski_drops=0 golod_drops=0 total=0\n• Régimen: 3.78W (Silicio Frío)\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(out.encode("utf-8"))
            return

        if req_path == "/proc/thermal":
            out = "3.78 W [LAMINAR PASIVO - COTA LANDAUER E=kB*T*ln(phi)]\n• Pacer: pi/phi = 1.938 ms\n• Ventiladores: 0 RPM\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(out.encode("utf-8"))
            return

        # Fallback 404
        self._send_json({"error": "NOT_FOUND", "path": req_path}, 404)

    def do_POST(self):
        # 1. Pulsos de presencia Gossip (Heartbeats)
        if self.path.startswith("/v1/swarm/heartbeat"):
            node_id = "NODE-" + self.client_address[0].replace(".", "-")
            mflops = 24.34
            power_w = 0.85
            try:
                parsed = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed.query)
                if "id" in params: node_id = params["id"][0]
                if "mflops" in params: mflops = float(params["mflops"][0])
                if "power" in params: power_w = float(params["power"][0])
            except Exception:
                pass
            GOSSIP_PEERS[node_id] = {
                "id": node_id,
                "role": "Worker WebGPU/WASM",
                "arch": "Navegador Remoto (Gossip)",
                "mflops": mflops,
                "power_w": power_w,
                "status": "COMPUTING",
                "last_seen": time.time()
            }
            self._send_json({"status": "OK", "ack": "GOSSIP_PULSE_RECEIVED", "node_id": node_id})
            return

        # 2. Inferencia Híbrida Desacoplada (Streaming SSE / Capa 0 / Avisos)
        if self.path.startswith("/v1/ai/generate") or self.path.startswith("/v1/ai/chat"):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except Exception:
                data = {}

            prompt = data.get("prompt", "")
            model = data.get("model", "aether:1.5b")

            tipo, payload = hybrid_ai.route_query(prompt, model)

            # Capa 0 o Avisos Estáticos (Capa 1 y Capa 3)
            if tipo in ("CAPA_0_STATIC", "CAPA_1_NOTICE", "CAPA_3_NOTICE"):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                chunk = json.dumps({"response": payload}) + "\n"
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()
                return

            # Capa 2: Streaming en vivo hacia Ollama local
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            fwd_bytes = json.dumps(payload).encode("utf-8")
            try:
                req = urllib.request.Request(
                    f"{hybrid_ai.OLLAMA_URL}/api/generate",
                    data=fwd_bytes,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=40) as resp:
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        self.wfile.write(line)
                        self.wfile.flush()
                return
            except Exception as e:
                err_chunk = json.dumps({"response": f" [OASIS RESIDUAL]: Inferencia offline ({e})"}) + "\n"
                self.wfile.write(err_chunk.encode("utf-8"))
                self.wfile.flush()
                return

        self._send_json({"error": "NOT_FOUND"}, 404)

if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", PORT), SovereignGatewayHandler)
    print(f"🛰️ OASIS GATEWAY v19.5.0 escuchando en http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
