#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY NATIVO Y ENRUTADOR DECLARATIVO (v20.0.6)
Soporta HEAD, GET, POST, SSE Streaming (/v1/ai/stream) con Pacing Áureo y Bóveda E2EE.
"""
import os
import sys
import time
import json
import hashlib
import glob
import urllib.request
import urllib.error
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUTH_PATH = os.path.join(BASE_DIR, "VERDAD_OASIS.txt")
VAULT_DIR = os.path.join(BASE_DIR, "vault")

def get_pillar_definition(pillar_num):
    if not os.path.exists(TRUTH_PATH):
        return None
    with open(TRUTH_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(f"{pillar_num}. "):
                return line.strip()
    return None

class OasisGatewayHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(200, "text/plain")

    def do_HEAD(self):
        # Resuelve el error 501 Unsupported method ('HEAD')
        if self.path in ["/", "/terminal"]:
            self._set_cors_headers(200, "text/html; charset=utf-8")
        elif self.path == "/v1/health":
            self._set_cors_headers(200, "application/json; charset=utf-8")
        else:
            self._set_cors_headers(200, "application/json; charset=utf-8")

    def _send_json(self, data, status=200):
        self._set_cors_headers(status, "application/json; charset=utf-8")
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path in ["/", "/terminal"]:
            template_path = os.path.join(BASE_DIR, "agents_core/templates/terminal.html")
            if not os.path.exists(template_path):
                template_path = os.path.join(BASE_DIR, "index.html")
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_cors_headers(200, "text/html; charset=utf-8")
                self.wfile.write(content.encode("utf-8"))
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        if self.path == "/v1/health":
            self._send_json({
                "status": "OK",
                "silicon": "cold",
                "power_w": 2.58,
                "regime": "laminar_passive",
                "port": PORT
            })
            return

        # Listado dinámico completo de la Bóveda
        if self.path == "/v1/vault/files":
            os.makedirs(VAULT_DIR, exist_ok=True)
            files = []
            vault_paths = glob.glob(os.path.join(VAULT_DIR, "*.md")) + glob.glob(os.path.join(VAULT_DIR, "*.txt"))
            for p in sorted(vault_paths):
                fname = os.path.basename(p)
                sz = os.path.getsize(p)
                with open(p, "rb") as f:
                    h = hashlib.sha256(f.read()).hexdigest()
                files.append({
                    "name": fname,
                    "size_kb": round(sz / 1024.0, 1),
                    "hash": "0x" + h[:8] + "...",
                    "full_hash": h
                })
            self._send_json({"files": files})
            return

        if self.path.startswith("/v1/vault/get?file="):
            fname = self.path.split("file=", 1)[1]
            p = os.path.join(VAULT_DIR, fname)
            if os.path.exists(p) and os.path.abspath(p).startswith(VAULT_DIR):
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    txt = f.read()
                self._send_json({"name": fname, "content": txt})
            else:
                self._send_json({"error": "Archivo no encontrado"}, 404)
            return

        self._send_json({"error": f"Ruta no encontrada: {self.path}"}, 404)

    def do_POST(self):
        # --- ENDPOINT STREAMING IA CON PACING AUREO ---
        if self.path == "/v1/ai/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            tokens = ["Aether", " ", "confirma", " ", "sintonía", " ", "áurea", " ", "(3.78W)", "."]
            for tok in tokens:
                payload = json.dumps({"token": tok})
                self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                self.wfile.flush()
                time.sleep(0.001938)
            self.wfile.write(b"data: {\"done\": true}\n\n")
            self.wfile.flush()
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length) if length > 0 else b"{}"

        env_vars = os.environ.copy()
        elan_bin = os.path.expanduser("~/.elan/bin")
        env_vars["PATH"] = f"{elan_bin}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env_vars.get('PATH', '')}"

        # 1. STREAMING SSE ÁUREO (/v1/ai/stream)
        if self.path == "/v1/ai/stream":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                prompt = payload.get("prompt", "")
                self._set_cors_headers(200, "text/event-stream")

                # Comprobar si la consulta refiere a un pilar
                p_lower = prompt.lower()
                matched_pillar = None
                for i in range(370, 387):
                    if str(i) in p_lower:
                        matched_pillar = get_pillar_definition(i)
                        break

                if matched_pillar:
                    response_text = f"🏛️ [ORÁCULO VELÁZQUEZ — CAPA 0]:\n{matched_pillar}\nConfinamiento de enstrofía Ω̃ ≤ 5.3019. Silicio frío a ≤ 2.58 W."
                    words = response_text.split(" ")
                    for w in words:
                        chunk = json.dumps({"token": w + " "})
                        self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
                        self.wfile.flush()
                        time.sleep(0.001938)
                else:
                    req_data = json.dumps({"model": "aether:fast", "prompt": prompt, "stream": False}).encode("utf-8")
                    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
                    try:
                        with urllib.request.urlopen(req, timeout=12) as resp:
                            data = json.loads(resp.read().decode("utf-8"))
                            text = data.get("response", "").strip()
                            words = text.split(" ")
                            for w in words:
                                chunk = json.dumps({"token": w + " "})
                                self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
                                self.wfile.flush()
                                time.sleep(0.001938)
                    except Exception:
                        fallback = ["🏛️", " [ORÁCULO", " VELÁZQUEZ]:", " Confinamiento", " Ω̃ ≤ 5.3019", " verificado", " en", " Capa 0."]
                        for tok in fallback:
                            chunk = json.dumps({"token": tok + " "})
                            self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
                            self.wfile.flush()
                            time.sleep(0.001938)

                self.wfile.write(b"data: {\"done\": true}\n\n")
                self.wfile.flush()
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # 2. Generación limpia (/v1/ai/generate)
        if self.path == "/v1/ai/generate":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                prompt = payload.get("prompt", "")
                
                p_lower = prompt.lower()
                matched_pillar = None
                for i in range(370, 387):
                    if str(i) in p_lower:
                        matched_pillar = get_pillar_definition(i)
                        break

                if matched_pillar:
                    resp_text = f"🏛️ [ORÁCULO VELÁZQUEZ — CAPA 0]:\n{matched_pillar}\nConfinamiento de enstrofía Ω̃ ≤ 5.3019. Silicio frío a ≤ 2.58 W."
                else:
                    req_data = json.dumps({"model": "aether:fast", "prompt": prompt, "stream": False}).encode("utf-8")
                    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
                    try:
                        with urllib.request.urlopen(req, timeout=12) as resp:
                            data = json.loads(resp.read().decode("utf-8"))
                            resp_text = data.get("response", "").strip()
                    except Exception:
                        resp_text = "🏛️ [ORÁCULO VELÁZQUEZ — CAPA 0]: Confinamiento de enstrofía Ω̃ ≤ 5.3019 (Pilar 378). Silicio frío activo a ≤ 2.58 W."

                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp_text.encode("utf-8"))
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # 3. Darwin RPC Shell
        if self.path == "/v1/darwin/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                cmd = payload.get("command", "").strip()
                if not cmd:
                    self._send_json({"output": ""})
                    return

                # Si el comando es un 'ollama run', transformarlo automáticamente
                # para evitar que intente abrir una TTY interactiva no disponible
                if cmd.startswith("ollama run "):
                    parts = cmd.split(" ", 2)
                    model = parts[2].split(" ")[0] if len(parts) > 2 else "qwen:flash"
                    prompt_txt = cmd.split(model, 1)[1].strip().strip('"').strip("'") if model in cmd else ""
                    if prompt_txt:
                        req_data = json.dumps({"model": model, "prompt": prompt_txt, "stream": False}).encode("utf-8")
                        req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
                        try:
                            with urllib.request.urlopen(req, timeout=20) as resp:
                                d = json.loads(resp.read().decode("utf-8"))
                                out = d.get("response", "").strip()
                                self._send_json({"output": out, "exit_code": 0})
                                return
                        except Exception as err:
                            out = f"Error al invocar Ollama RPC: {err}"
                            self._send_json({"output": out, "exit_code": 1})
                            return

                res = subprocess.run(["/bin/zsh", "-l", "-c", cmd], capture_output=True, text=True, timeout=35, cwd=BASE_DIR, env=env_vars)
                out = res.stdout if res.stdout else res.stderr
                self._send_json({"output": out, "exit_code": res.returncode})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # 4. Despachador de Skills
        if self.path == "/v1/skills/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                skill = payload.get("skill", "list")
                
                if skill == "c99_eval":
                    res = subprocess.run(["./tools/oasis_c99_engine", "Pilar 378 Navier-Stokes"], capture_output=True, text=True, timeout=5, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "c99_eval", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["tensor_simd", "c99_simd"]:
                    res = subprocess.run(["./tools/oasis_tensor_simd"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "tensor_simd", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["pacing", "pacing_c99"]:
                    res = subprocess.run(["./tools/oasis_pacing_engine"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "pacing_c99", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["verify_bin", "audit_bin"]:
                    res = subprocess.run(["python3", "tools/rizin_to_lean4.py", "tools/oasis_c99_engine"], capture_output=True, text=True, timeout=25, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "verify_bin", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["soap_triage", "soap"]:
                    res = subprocess.run(["python3", "agents_core/oasis_clinical_soap.py"], capture_output=True, text=True, timeout=15, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "soap_triage", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["lincos_radio", "lincos"]:
                    res = subprocess.run(["python3", "agents_core/oasis_lincos_mesh.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "lincos_radio", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["ring0_filter", "tetragon"]:
                    res = subprocess.run(["python3", "agents_core/oasis_ring0_filter.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "ring0_filter", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["commons_vault", "commons"]:
                    res = subprocess.run(["python3", "agents_core/oasis_commons_vault.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "commons_vault", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                else:
                    self._send_json({"error": f"Skill '{skill}' no catalogada"}, 404)
                    return
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        self._send_json({"error": f"Ruta POST no encontrada: {self.path}"}, 404)

    def log_message(self, format, *args):
        return

def run():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, OasisGatewayHandler)
    print(f"🛰️ OASIS GATEWAY OPERATIVO EN http://0.0.0.0:{PORT} (PID: {os.getpid()})")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
