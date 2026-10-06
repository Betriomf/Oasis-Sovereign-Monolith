#!/usr/bin/env python3
"""
OASIS LOCAL DAEMON (PUERTO 8765)
Enlace directo de silicio entre la Terminal Web y tu MacBook Air.
"""
import os
import json
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8765
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODELO = "oasis-edge:1.5b"

class LocalNodeHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-hw-key, x-api-key")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-hw-key, x-api-key")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/v1/local/telemetry"):
            # Métricas nativas del Mac (Darwin)
            uname = subprocess.check_output(["uname", "-srm"]).decode().strip()
            load = subprocess.check_output(["sysctl", "-n", "vm.loadavg"]).decode().strip()
            self._send_json({
                "status": "ONLINE",
                "silicio": "MacBook Air (Darwin x86_64)",
                "kernel": uname,
                "loadavg": load,
                "ollama_active": True
            })
        else:
            self._send_json({"error": "Ruta no encontrada"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length).decode()) if content_length > 0 else {}

        # 1. Inferencia Directa con Ollama (Latencia Ultrabaja)
        if self.path == "/v1/local/ai":
            prompt = body.get("prompt", "")
            chosen_model = "qwen2.5:7b-instruct-q4_K_M" if "--7b" in prompt else MODELO
            prompt_clean = prompt.replace("--7b", "").strip()

            ollama_body = json.dumps({
                "model": chosen_model,
                "prompt": prompt_clean,
                "stream": False,
                "keep_alive": "60m",
                "options": {"temperature": 0.23, "num_predict": 200, "num_thread": 6}
            }).encode()

            try:
                req = urllib.request.Request(OLLAMA_API, data=ollama_body, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=40) as resp:
                    ai_reply = json.loads(resp.read().decode()).get("response", "").strip()
                self._send_json({
                    "status": "SUCCESS_DIRECT_SILICON",
                    "model_used": chosen_model,
                    "response": ai_reply
                })
            except Exception as e:
                self._send_json({"error": f"Error conectando a Ollama: {e}"}, status=500)
            return

        # 2. Ejecución Nativa de Comandos en el Mac
        if self.path == "/v1/local/exec":
            cmd = body.get("cmd", "")
            try:
                res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode()
                self._send_json({"output": res})
            except subprocess.CalledProcessError as e:
                self._send_json({"output": e.output.decode()})
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    print(f"🛰️  [OASIS LOCAL DAEMON]: Escuchando en http://127.0.0.1:{PORT}")
    print("🔒 Enlace directo con la terminal web activo bajo silicio frío.")
    server = HTTPServer(("127.0.0.1", PORT), LocalNodeHandler)
    server.serve_forever()
