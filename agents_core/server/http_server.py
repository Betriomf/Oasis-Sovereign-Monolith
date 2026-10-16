# -*- coding: utf-8 -*-
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from routes.static_routes import handle_static_get
from routes.system_routes import handle_system_get, handle_system_post
from routes.quantum_routes import handle_quantum_get, handle_quantum_post

class OasisRouterHandler(BaseHTTPRequestHandler):
    kernel_version = "v16.3.0-ModularHurd"

    def _respond(self, status, content_type, payload):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        for handler in (
            lambda: handle_static_get(self.path, self.kernel_version),
            lambda: handle_system_get(self.path, self.kernel_version),
            lambda: handle_quantum_get(self.path)
        ):
            resp = handler()
            if resp:
                self._respond(*resp)
                return
        self._respond(404, "application/json", json.dumps({"error": "NOT_FOUND"}).encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        for handler in (
            lambda: handle_system_post(self.path, body),
            lambda: handle_quantum_post(self.path, body)
        ):
            resp = handler()
            if resp:
                self._respond(*resp)
                return
        self._respond(404, "application/json", json.dumps({"error": "ENDPOINT_NOT_FOUND"}).encode("utf-8"))

def run_server(port: int, version: str):
    OasisRouterHandler.kernel_version = version
    server = HTTPServer(("0.0.0.0", port), OasisRouterHandler)
    print(f"🔒 OASIS GATEWAY MODULAR [{version}] activo en puerto {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido limpiamente.")
