#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server, socketserver, json, urllib.request, subprocess, time, os

PORT = 8080
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def ensure_ollama():
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200: return True
    except Exception: pass
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

class OasisGatewayHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            rust_output = "Motor Rust No Detectado"
            paths = [
                os.path.expanduser("~/oasis_vacuum/oasis-core-simulation"),
                os.path.expanduser("~/Oasis-Sovereign-Monolith/target/release/oasis-core-simulation"),
                os.path.expanduser("~/Oasis-Sovereign-Monolith/oasis-core-simulation/target/release/oasis-core-simulation")
            ]
            for p in paths:
                if os.path.exists(p):
                    try:
                        res = subprocess.run([p], capture_output=True, text=True, timeout=2)
                        rust_output = res.stdout.strip()
                        break
                    except Exception as e: rust_output = str(e)

            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "ONLINE", "rust_kernel": rust_output, "port": PORT}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/chat":
            body = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8")
            data = json.loads(body)
            prompt_text = data.get("prompt", "")
            ensure_ollama()

            payload = {
                "model": "oasis-aether-soup:1.5b",
                "prompt": prompt_text,
                "stream": False,
                "keep_alive": "10m",
                "options": { "temperature": 0.1, "num_predict": 256, "num_thread": 4 }
            }

            req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                self._set_headers(200)
                self.wfile.write(json.dumps({"response": res.get("response", "")}).encode("utf-8"))

if __name__ == "__main__":
    ensure_ollama()
    with ReusableTCPServer(("0.0.0.0", PORT), OasisGatewayHandler) as httpd:
        httpd.serve_forever()
