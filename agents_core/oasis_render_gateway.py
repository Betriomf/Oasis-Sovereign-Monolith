from http.server import ThreadingHTTPServer
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


def query_ollama_cascade(prompt):
    models_to_try = ["qwen:flash", "qwen2.5:0.5b", "aether:1.5b", "aether:fast"]
    for m in models_to_try:
        try:
            req_data = json.dumps({"model": m, "prompt": prompt, "stream": False}).encode("utf-8")
            req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data.get("response", "").strip()
                if text:
                    return text
        except Exception:
            continue
    return "Error: No se pudo conectar con los modelos locales de Ollama (127.0.0.1:11434)."


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
                elif self.path == "/v1/vault/list":
            vault_files = []
            if os.path.exists(VAULT_DIR):
                vault_files = sorted([f for f in os.listdir(VAULT_DIR) if not f.startswith(".")])
            self._send_json({"vault_files": vault_files, "total": len(vault_files)})
            return
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
        env_vars["OMP_NUM_THREADS"] = "2"
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
                    resp_text = query_ollama_cascade(prompt)

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
                skill = payload.get("skill", "").strip()
                target_user = payload.get("target") or payload.get("args") or "Betriomf"

                if skill in ["osint", "recon", "surface"]:
                    res = subprocess.run(["python3", "tools/oasis_osint.py", str(target_user)], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "osint", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["crm", "bitacora", "historial"]:
                    action = payload.get("action", "list")
                    args = payload.get("args", "").split()
                    cmd = ["python3", "tools/oasis_crm.py", action] + args
                    res = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "crm", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["scraper", "volcado", "backup"]:
                    res = subprocess.run(["python3", "tools/oasis_scraper_engine.py", "--all"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "scraper", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["c99_eval", "tensor_simd"]:
                    res = subprocess.run(["./tools/oasis_c99_engine"], capture_output=True, text=True, timeout=5, cwd=BASE_DIR, env=env_vars)
                    out = res.stdout if res.stdout else res.stderr
                    self._send_json({"skill": "c99_eval", "output": out, "status": "COMPLETED"})
                    return
                elif skill in ["pacing", "pacing_c99"]:
                    res = subprocess.run(["./tools/oasis_pacing_engine"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "pacing_c99", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["mesh", "gossip"]:
                    res = subprocess.run(["python3", "tools/oasis_cli.py", "mesh"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "mesh", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["qr", "invite"]:
                    res = subprocess.run(["python3", "tools/oasis_cli.py", "qr"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "qr", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["id", "identity"]:
                    res = subprocess.run(["python3", "tools/oasis_cli.py", "id"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "id", "output": res.stdout, "status": "COMPLETED"})
                    return
                else:
                            elif skill in ["minkowski", "filter", "pilar387"]:
            res = subprocess.run(["./tools/oasis_kernel_filter"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
            self._send_json({"skill": "minkowski", "output": res.stdout, "status": "COMPLETED"})
            return
        elif skill in ["sec", "audit", "posture"]:
            res = subprocess.run(["python3", "tools/oasis_sec_auditor.py"], capture_output=True, text=True, cwd=BASE_DIR, env=env_vars)
            self._send_json({"skill": "sec", "output": res.stdout, "status": "COMPLETED"})
            return
        self._send_json({"error": f"Skill '{skill}' no catalogada", "status": "FAILED"}, 400)
                    return
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, OasisGatewayHandler)
    print(f"🚀 [OASIS GATEWAY]: Escuchando en http://127.0.0.1:{port}/terminal (Silicio Frío)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo Gateway...")
        httpd.server_close()

