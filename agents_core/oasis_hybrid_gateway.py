#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server, socketserver, json, urllib.request, subprocess, os

PORT = 8080
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class OasisHybridHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            # 1. Comprobar ejecutable en Rust
            rust_bin = os.path.expanduser("~/oasis_vacuum/oasis-core-simulation")
            rust_status = "Motor Rust Activo" if os.path.exists(rust_bin) else "Rust No Detectado"
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "ONLINE",
                "engine": "Oasis Sovereign Native Gateway",
                "rust_kernel": rust_status,
                "port": PORT
            }).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Ruta no encontrada"}')

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            prompt = data.get("prompt", "")

            # 2. Enviar consulta directamente a Ollama local
            payload = {
                "model": "qwen2.5:7b-instruct-q4_K_M",
                "prompt": f"[SISTEMA OASIS OS - MACBOOK]:\n{prompt}",
                "stream": False,
                "options": { "temperature": 0.1, "num_thread": 4 }
            }

            try:
                req = urllib.request.Request(
                    OLLAMA_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"response": res.get("response", "")}).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", PORT), OasisHybridHandler) as httpd:
        print(f"⚡ [OASIS GATEWAY HÍBRIDO]: Activo en http://127.0.0.1:{PORT}")
        httpd.serve_forever()
