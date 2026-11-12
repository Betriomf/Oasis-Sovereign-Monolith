#!/usr/bin/env python3
import os
import sys
import json
import time
import hashlib
import secrets
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

os.environ["OMP_NUM_THREADS"] = "2"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
TEMPLATE_DIR = os.path.join(BASE_DIR, "agents_core", "templates")

L402_CHALLENGES = {}

class OasisGatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200, extra_headers=None):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Silicon-Power", "<= 2.58 W")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
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
                "l402_gateway": "ACTIVE",
                "port": port
            })
            return

        elif self.path == "/v1/papers/paper_b.pdf":
            pdf_path = os.path.join(BASE_DIR, "papers", "paper_b_millennium_regularity.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(len(pdf_data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(pdf_data)
            else:
                self._send_json({"error": "PDF aún no compilado (pdflatex ausente o build pendiente)"}, 404)
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

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(raw_body)
        except Exception:
            self._send_json({"error": "JSON malformado", "status": "FAILED"}, 400)
            return

        if self.path.startswith("/v1/swarm/heartbeat"):
            self._send_json({"status": "HEARTBEAT_ACK", "silicon": "cold", "power_w": 0.85})
            return

        elif self.path == "/v1/l402/infer":
            auth = self.headers.get("Authorization", "")
            paid = False
            verified_hash = ""

            if auth.startswith("L402 ") and ":" in auth:
                try:
                    _, creds = auth.split(" ", 1)
                    macaroon_hash, preimage_hex = creds.split(":", 1)
                    calc_hash = hashlib.sha256(bytes.fromhex(preimage_hex.strip())).hexdigest()
                    if calc_hash == macaroon_hash.strip() and calc_hash in L402_CHALLENGES:
                        paid = True
                        verified_hash = calc_hash
                        del L402_CHALLENGES[calc_hash]
                except Exception:
                    paid = False

            if not paid:
                secret_preimage = secrets.token_hex(32)
                pay_hash = hashlib.sha256(bytes.fromhex(secret_preimage)).hexdigest()
                L402_CHALLENGES[pay_hash] = time.time()
                invoice_mock = f"lnbc50n1oasis0pilar3870{pay_hash[:24]}"
                self._send_json(
                    {
                        "error": "Payment Required (L402 Lightning Micropayment)",
                        "price_sats": 5,
                        "payment_hash": pay_hash,
                        "invoice": invoice_mock,
                        "sandbox_preimage_for_test": secret_preimage
                    },
                    status=402,
                    extra_headers={"WWW-Authenticate": f'L402 macaroon="{pay_hash}", invoice="{invoice_mock}"'}
                )
                return

            prompt = payload.get("prompt", "Confirma recepción L402.")
            model = payload.get("model", "qwen2.5:1.5b")
            req_ai = urllib.request.Request(
                "http://127.0.0.1:11434/api/generate",
                data=json.dumps({"model": model, "prompt": prompt, "stream": False, "keep_alive": -1, "options": {"num_thread": 2}}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req_ai, timeout=90) as r:
                    ans = json.loads(r.read().decode("utf-8")).get("response", "")
                self._send_json({
                    "status": "SETTLED_AND_COMPLETED",
                    "payment_hash": verified_hash,
                    "model": model,
                    "response": ans
                })
            except Exception as e:
                self._send_json({"error": f"Motor IA ocupado: {e}", "status": "FAILED"}, 502)
            return

        elif self.path == "/v1/skill":
            skill = payload.get("skill", "")
            prompt = payload.get("prompt", "")
            env_vars = os.environ.copy()
            env_vars["OMP_NUM_THREADS"] = "2"

            if skill in ["paper", "build_paper", "paper_b"]:
                res = subprocess.run(["bash", "tools/build_paper_b.sh"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                out = res.stdout + ("\n" + res.stderr if res.stderr else "")
                status = "COMPLETED" if res.returncode == 0 else "FAILED"
                self._send_json({"skill": "paper", "output": out, "status": status})
                return
            elif skill in ["minkowski", "filter", "pilar387"]:
                res = subprocess.run(["./tools/oasis_kernel_filter"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "minkowski", "output": res.stdout, "status": "COMPLETED"})
                return
            elif skill in ["sec", "audit", "posture"]:
                res = subprocess.run([sys.executable, "tools/oasis_sec_auditor.py"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "sec", "output": res.stdout, "status": "COMPLETED"})
                return
            elif skill in ["ia", "ask", "llm"]:
                if not prompt:
                    self._send_json({"error": "Se requiere prompt"}, 400)
                    return
                req_ai = urllib.request.Request(
                    "http://127.0.0.1:11434/api/generate",
                    data=json.dumps({"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False, "keep_alive": -1, "options": {"num_thread": 2}}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                try:
                    with urllib.request.urlopen(req_ai, timeout=90) as r:
                        ans = json.loads(r.read().decode("utf-8")).get("response", "")
                    self._send_json({"skill": "ia", "output": ans, "status": "COMPLETED"})
                except Exception as e:
                    self._send_json({"error": str(e), "status": "FAILED"}, 502)
                return
            elif skill in ["crm"]:
                res = subprocess.run([sys.executable, "tools/oasis_crm.py", "list"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                self._send_json({"skill": "crm", "output": res.stdout, "status": "COMPLETED"})
                return
            else:
                self._send_json({"error": f"Skill '{skill}' no catalogada", "status": "FAILED"}, 404)
                return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    httpd = ThreadedHTTPServer(("127.0.0.1", port), OasisGatewayHandler)
    print(f"🚀 [OASIS GATEWAY + L402]: Escuchando en http://127.0.0.1:{port}/terminal")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
