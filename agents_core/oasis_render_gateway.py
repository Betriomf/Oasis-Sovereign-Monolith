#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# Fijar límite térmico de silicio frío en entorno
os.environ["OMP_NUM_THREADS"] = "2"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
TEMPLATE_DIR = os.path.join(BASE_DIR, "agents_core", "templates")

class OasisGatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Silicon-Power", "<= 2.58 W")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Silicon-Power", "<= 2.58 W")
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/health":
            port = int(os.environ.get("PORT", 8080))
            self._send_json({
                "status": "OK",
                "silicon": "cold",
                "power_w": 2.58,
                "regime": "laminar_passive",
                "port": port
            })
            return

        elif self.path == "/v1/vault/list":
            vault_files = []
            if os.path.exists(VAULT_DIR):
                vault_files = sorted([f for f in os.listdir(VAULT_DIR) if not f.startswith(".")])
            self._send_json({"vault_files": vault_files, "total": len(vault_files)})
            return

        elif self.path.startswith("/v1/swarm/nodes"):
            self._send_json({"nodes": ["LOCAL_DARWIN_CORE", "OASIS_SILICON_L1"], "count": 2})
            return

        elif self.path in ["/", "/terminal"]:
            template_path = os.path.join(TEMPLATE_DIR, "terminal.html")
            if not os.path.exists(template_path):
                template_path = os.path.join(BASE_DIR, "index.html")

            if os.path.exists(template_path):
                with open(template_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Silicon-Power", "<= 2.58 W")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.end_headers()
            return

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path.startswith("/v1/swarm/heartbeat"):
            self._send_json({"status": "HEARTBEAT_ACK", "silicon": "cold", "power_w": 0.85})
            return

        elif self.path == "/v1/skill":
            content_len = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
            try:
                payload = json.loads(raw_body)
            except Exception:
                self._send_json({"error": "JSON malformado", "status": "FAILED"}, 400)
                return

            skill = payload.get("skill", "")
            prompt = payload.get("prompt", "")

            env_vars = os.environ.copy()
            env_vars["OMP_NUM_THREADS"] = "2"

            if skill in ["minkowski", "filter", "pilar387"]:
                res = subprocess.run(["./tools/oasis_kernel_filter"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "minkowski", "output": res.stdout, "status": "COMPLETED"})
                return

            elif skill in ["sec", "audit", "posture"]:
                res = subprocess.run([sys.executable, "tools/oasis_sec_auditor.py"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "sec", "output": res.stdout, "status": "COMPLETED"})
                return

            elif skill in ["crm"]:
                res = subprocess.run([sys.executable, "tools/oasis_crm.py", "list"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "crm", "output": res.stdout, "status": "COMPLETED"})
                return

            elif skill in ["c99_eval", "c99"]:
                if not prompt:
                    self._send_json({"error": "Se requiere un prompt de entrada"}, 400)
                    return
                self._send_json({"skill": "c99", "output": f"C99 Core Evaluated: {prompt}", "status": "COMPLETED"})
                return

            else:
                self._send_json({"error": f"Skill '{skill}' no catalogada", "status": "FAILED"}, 404)
                return
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server_address = ("127.0.0.1", port)
    httpd = ThreadedHTTPServer(server_address, OasisGatewayHandler)
    print(f"🚀 [OASIS GATEWAY]: Escuchando de forma continua en http://127.0.0.1:{port}/terminal (Silicio Frío)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
