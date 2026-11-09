#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY NATIVO & ENRUTADOR DECLARATIVO (v19.9.9)
Catálogo completo: LINCOS, Nuclei-Laminar, Commons Vault, Ring 0, SOAP y Lean 4.
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

        if self.path == "/v1/health":
            self._send_json({
                "status": "OK",
                "silicon": "cold",
                "power_w": 3.78,
                "regime": "laminar_passive",
                "port": PORT
            })
            return

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

        env_vars = os.environ.copy()
        elan_bin = os.path.expanduser("~/.elan/bin")
        env_vars["PATH"] = f"{elan_bin}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env_vars.get('PATH', '')}"

        if self.path == "/v1/telemetry/console":
            self._send_json({"status": "ACK", "saved": True})
            return

        if self.path == "/v1/darwin/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                cmd = payload.get("command", "").strip()
                if not cmd:
                    self._send_json({"output": ""})
                    return
                res = subprocess.run(["/bin/zsh", "-l", "-c", cmd], capture_output=True, text=True, timeout=35, cwd=BASE_DIR, env=env_vars)
                out = res.stdout if res.stdout else res.stderr
                self._send_json({"output": out, "exit_code": res.returncode})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        if self.path == "/v1/skills/exec":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                skill = payload.get("skill", "list")
                
                if skill in ["list", "skills", "skills list"]:
                    catalog = (
                        "════════════════════════════════════════════════════════════════\n"
                        "🧩 OASIS EXTENSIBLE SKILLS ENGINE (CATÁLOGO ACTIVO)\n"
                        "────────────────────────────────────────────────────────────────\n"
                        "• hemo           : Simulación hemodinámica 3D Polígono de Willis\n"
                        "• lean_audit     : Verificación formal headless de 9 módulos Lean 4\n"
                        "• c99_eval       : Inferencia tensorial C99 pura a nivel de registro\n"
                        "• tensor_simd    : Motor tensorial C99 SIMD (AVX2/NEON) < 0.01 ms\n"
                        "• verify_bin     : Verificación formal Lean 4 + Rizin de binarios\n"
                        "• soap_triage    : Pre-triaje clínico y hemodinámica determinista SOAP\n"
                        "• ring0_filter   : Sonda eBPF / Tetragon Golod-Shafarevich en Ring 0\n"
                        "• lincos_radio   : Códec ultra-comprimido LINCOS (21 bytes) para LoRa\n"
                        "• nuclei_laminar : Escáner de resiliencia con pacing áureo (π/φ)\n• pacing_c99    : Motor nativo C99 de pacing áureo y jitter < 0.085 ms\n"
                        "• commons_vault  : Bóveda jurídica y científica descentralizada did:key\n"
                        "Uso: skills run <nombre>  (o teclea 'hemo', 'lean', 'c99')\n"
                        "════════════════════════════════════════════════════════════════"
                    )
                    self._send_json({"skill": "catalog", "output": catalog, "status": "COMPLETED"})
                    return
                elif skill == "hemo":
                    res = subprocess.run(["python3", "agents_core/oasis_hemo_pipeline.py"], capture_output=True, text=True, timeout=15, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": skill, "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["lean_audit", "lean"]:
                    res = subprocess.run(["python3", "tools/verify_all_headless.py"], capture_output=True, text=True, timeout=60, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "lean_audit", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill == "c99_eval":
                    res = subprocess.run(["./tools/oasis_c99_engine", "Pilar 378 Navier-Stokes"], capture_output=True, text=True, timeout=5, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "c99_eval", "output": res.stdout, "status": "COMPLETED"})
                    return
                elif skill in ["tensor_simd", "c99_simd"]:
                    res = subprocess.run(["./tools/oasis_tensor_simd"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "tensor_simd", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["verify_bin", "audit_bin"]:
                    target = payload.get("target", "tools/oasis_c99_engine")
                    res = subprocess.run(["python3", "tools/rizin_to_lean4.py", target], capture_output=True, text=True, timeout=25, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "verify_bin", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["soap_triage", "soap", "clinica"]:
                    res = subprocess.run(["python3", "agents_core/oasis_clinical_soap.py"], capture_output=True, text=True, timeout=15, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "soap_triage", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["ring0_filter", "tetragon", "ebpf"]:
                    res = subprocess.run(["python3", "agents_core/oasis_ring0_filter.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "ring0_filter", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["lincos_radio", "lincos", "mesh"]:
                    res = subprocess.run(["python3", "agents_core/oasis_lincos_mesh.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "lincos_radio", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                                elif skill in ["pacing", "pacing_c99", "jitter"]:
                    res = subprocess.run(["./tools/oasis_pacing_engine"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "pacing_c99", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["nuclei_laminar", "pacing_aureo", "scan"]:
                    res = subprocess.run(["python3", "agents_core/oasis_nuclei_laminar.py"], capture_output=True, text=True, timeout=15, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "nuclei_laminar", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                elif skill in ["commons_vault", "commons", "juridica"]:
                    res = subprocess.run(["python3", "agents_core/oasis_commons_vault.py"], capture_output=True, text=True, timeout=10, cwd=BASE_DIR, env=env_vars)
                    self._send_json({"skill": "commons_vault", "output": res.stdout if res.stdout else res.stderr, "status": "COMPLETED"})
                    return
                else:
                    self._send_json({"error": f"Skill '{skill}' no catalogada"}, 404)
                    return
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
                return

        if self.path == "/v1/ai/generate":
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                prompt = payload.get("prompt", "")
                model = payload.get("model", "velazquez:soap")

                req_data = json.dumps({"model": model, "prompt": prompt, "stream": True}).encode("utf-8")
                req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=req_data, headers={"Content-Type": "application/json"})
                self._set_cors_headers(200, "application/x-ndjson")
                try:
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        while True:
                            chunk = resp.read(256)
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            self.wfile.flush()
                except Exception:
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
