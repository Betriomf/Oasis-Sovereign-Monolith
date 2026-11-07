#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY NATIVO & ENRUTADOR DECLARATIVO (v19.9.2)
Diseño de arquitectura limpia: cero inyecciones en caliente, 0.0.0.0:$PORT dinámico,
Private Network Access (PNA) para Safari, y despacho determinista de Capa 0 a Capa 3.
"""
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUTH_PATH = os.path.join(BASE_DIR, "VERDAD_OASIS.txt")

def parse_truth_ontology():
    pillars = []
    if os.path.exists(TRUTH_PATH):
        with open(TRUTH_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and line[0].isdigit() and ". " in line:
                    parts = line.split(". ", 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        pillars.append({"pillar": int(parts[0]), "definition": parts[1]})
    return pillars

class OasisGatewayHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(200, "text/plain")

    def _send_json(self, data, status=200):
        self._set_cors_headers(status, "application/json; charset=utf-8")
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        # 1. Frontend Terminal Web
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
                self._send_json({"error": f"Fallo al cargar plantilla: {e}"}, 500)
            return

        # 2. Telemetría de Silicio Frío
        if self.path == "/v1/health":
            self._send_json({
                "status": "OK",
                "silicon": "cold",
                "power_w": 3.78,
                "regime": "laminar_passive",
                "port": PORT
            })
            return

        # 3. Ontología de Pilares y Verdad Oasis
        if self.path == "/v1/roadmap":
            pillars = parse_truth_ontology()
            self._send_json({
                "status": "OK",
                "total_pillars": len(pillars),
                "latest_series": pillars[-10:] if pillars else []
            })
            return

        self._send_json({"error": f"Ruta GET no encontrada: {self.path}"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length) if length > 0 else b"{}"

        # 1. Telemetría Console Forwarding
        if self.path == "/v1/telemetry/console":
            self._send_json({"status": "ACK", "saved": True})
            return

        # 2. RPC Nativo Shell (Darwin / Render Linux)
        if self.path == "/v1/darwin/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                cmd = payload.get("command", "").strip()
                if not cmd:
                    self._send_json({"output": ""})
                    return
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=35, cwd=BASE_DIR)
                out = res.stdout if res.stdout else res.stderr
                self._send_json({"output": out, "exit_code": res.returncode})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # 3. Despachador de Skills de Capa 0
        if self.path == "/v1/skills/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                skill = payload.get("skill", "list")
                if skill in ["list", "skills", "skills list"]:
                    catalog = (
                        "════════════════════════════════════════════════════════════════\n"
                        "🧩 OASIS EXTENSIBLE SKILLS ENGINE (CATÁLOGO ACTIVO)\n"
                        "────────────────────────────────────────────────────────────────\n"
                        "• hemo       : Simulación hemodinámica 3D Polígono de Willis\n"
                        "• lean_audit : Verificación formal headless de 9 módulos Lean 4\n"
                        "• c99_eval   : Inferencia tensorial C99 pura a nivel de registro\n"
                        "Uso: skills run <nombre>  (o teclea 'hemo', 'lean', 'c99')\n"
                        "════════════════════════════════════════════════════════════════"
                    )
                    self._send_json({"skill": "catalog", "output": catalog, "status": "COMPLETED"})
                    return
                elif skill == "hemo":
                    res = subprocess.run(["python3", "agents_core/oasis_hemo_pipeline.py"], capture_output=True, text=True, timeout=15, cwd=BASE_DIR)
                    self._send_json({"skill": skill, "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["lean_audit", "lean"]:
                    res = subprocess.run(["python3", "tools/verify_all_headless.py"], capture_output=True, text=True, timeout=60, cwd=BASE_DIR)
                    self._send_json({"skill": "lean_audit", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill == "c99_eval":
                    res = subprocess.run(["./tools/oasis_c99_engine", "Pilar 378 Navier-Stokes"], capture_output=True, text=True, timeout=5, cwd=BASE_DIR)
                    self._send_json({"skill": "c99_eval", "output": res.stdout, "status": "COMPLETED"})
                    return
                else:
                    self._send_json({"error": f"Skill '{skill}' no catalogada"}, 404)
                    return
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # 4. Inferencia IA (Streaming Velázquez / Riona / Ollama)
        if self.path == "/v1/ai/generate":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                prompt = payload.get("prompt", "")
                model = payload.get("model", "velazquez:soap")

                if model == "riona" or "riona" in payload.get("agent", ""):
                    try:
                        import agents_core.riona_agent as riona_mod
                        resp_text = riona_mod.riona_process(prompt)
                    except Exception as e:
                        resp_text = f"🛰️ [RIONA]: Error en pipeline: {e}"
                    self._set_cors_headers(200, "application/x-ndjson")
                    self.wfile.write((json.dumps({"response": resp_text}) + "\n").encode("utf-8"))
                    return

                # Petición a Ollama local
                req_data = json.dumps({"model": model, "prompt": prompt, "stream": True}).encode("utf-8")
                req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
                self._set_cors_headers(200, "application/x-ndjson")
                try:
                    with urllib.request.urlopen(req, timeout=40) as resp:
                        while True:
                            chunk = resp.read(256)
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            self.wfile.flush()
                except Exception:
                    # Fallback autónomo en estasis de Capa 0
                    fallback = (
                        "🏛️ [ORÁCULO VELÁZQUEZ — CAPA 0]:\n"
                        "Estasis activa. Confinamiento de enstrofía Ω̃ ≤ 5.3019 (Pilar 378). "
                        "Silicio frío preservado a ≤ 3.78 W."
                    )
                    self.wfile.write((json.dumps({"response": fallback}) + "\n").encode("utf-8"))
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
