#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS SOVEREIGN OS — ORQUESTADOR MODULAR v16.3.0-HurdMaster
Arquitectura desacoplada:
- Frontend aislado en agents_core/templates/*.html
- Backend cuántico aislado en agents_core/handlers/quantum_engine.py
- Auto-parcheo AST aislado en agents_core/handlers/system_patcher.py
"""

import os
import json
import socket
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
from handlers.quantum_engine import enqueue_circuit, get_circuit_status
from handlers.system_patcher import read_source_file, apply_code_patch

KERNEL_VERSION = "v16.3.0-ModularHurd"
PORT = int(os.environ.get("PORT", 8080))
IS_RENDER = os.environ.get("RENDER") == "true"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

def load_template(filename: str) -> str:
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

class OasisModularGatewayHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_GET(self):
        # 1. Rutas Frontend (Cargadas dinámicamente desde templates/)
        if self.path in ("/", "/terminal") or self.path.startswith("/terminal?"):
            tpl = load_template("terminal.html").replace("{{KERNEL_VERSION}}", KERNEL_VERSION)
            self._send_html(tpl)
        elif self.path.startswith("/sheet"):
            self._send_html(load_template("sheet.html"))
        elif self.path in ("/oasis_tab", "/extension/oasis_tab.html"):
            self._send_html(load_template("telemetry.html"))
        elif self.path in ("/v86_linux", "/linux"):
            self._send_html(load_template("v86_linux.html"))

        # 2. Rutas de API y Sistema
        elif self.path.startswith("/v1/system/source"):
            query_file = self.path.split("file=")[-1] if "file=" in self.path else "agents_core/oasis_render_gateway.py"
            res = read_source_file(query_file)
            status_code = 404 if "error" in res else 200
            self._send_json(res, status=status_code)

        elif self.path in ("/telemetry", "/v1/agent/status"):
            self._send_json({
                "status": "ONLINE",
                "version": KERNEL_VERSION,
                "power_watts": 4.18,
                "silicon_power": 4.18,
                "cpu_efficient_load": 12.4,
                "entropy_asymmetry": "0.00 J/K·s (Adiabático)",
                "arpanet_mesh": 23,
                "hardware_id": "OASIS-HW-468F6F695BDB"
            })
        elif self.path.startswith("/v1/quantum/status"):
            task_id = self.path.split("task_id=")[-1] if "task_id=" in self.path else ""
            self._send_json(get_circuit_status(task_id))
        else:
            self._send_json({"error": "NOT_FOUND"}, status=404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        # 1. Auto-Patching con Linter AST
        if self.path == "/v1/system/patch":
            target = body.get("target_file", "agents_core/oasis_render_gateway.py")
            content = body.get("content", "")
            reload_srv = body.get("hot_reload", True)
            res = apply_code_patch(target, content, reload_srv)
            status_code = 200 if res.get("success") else 400
            self._send_json(res, status=status_code)
            return

        # 2. Encolado Cuántico
        elif self.path == "/v1/quantum/run":
            c_type = body.get("circuit", "bell")
            shots = body.get("shots", 1024)
            node_id = body.get("node_id", "ANON")
            t_id = enqueue_circuit(c_type, shots, node_id)
            self._send_json({"status": "QUEUED", "task_id": t_id})
            return

        self._send_json({"status": "PROCESSED"}, status=200)

def main():
    server = HTTPServer(("0.0.0.0", PORT), OasisModularGatewayHandler)
    scheme = "http"
    print(f"🔒 OASIS GATEWAY MODULAR {KERNEL_VERSION} activo en {scheme}://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")

if __name__ == "__main__":
    main()
