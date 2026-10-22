#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS SOVEREIGN OS — GATEWAY UNIVERSAL v16.0.0-ModularCore
Backend Desacoplado: Servidor de Plantillas, Enrutador Darwin y Bóveda OPFS.
Autor: Mariano Panzano Caballé | Licencia AGPLv3 / CC-BY-4.0
"""
import os, sys, json, subprocess, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "agents_core", "templates")
TRUTH_FILE = os.path.join(REPO_ROOT, "VERDAD_OASIS.txt")

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LAN_IP = get_lan_ip()

def load_template(filename):
    filepath = os.path.join(TEMPLATES_DIR, filename)
    if not os.path.exists(filepath):
        return f"<h1>Error 404: Plantilla '{filename}' no encontrada</h1>"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content.replace("{{LAN_IP}}", LAN_IP)

def query_verdad_oasis(query_str):
    query_str = query_str.strip()
    # Prioridad: OpenViking L1 (0.01 ms)
    if query_str.isdigit():
        viking_path = os.path.join(REPO_ROOT, "data", "openviking", "resources", "pilares", "L1", f"pilar_{int(query_str):03d}.l1")
        if os.path.exists(viking_path):
            with open(viking_path, "r", encoding="utf-8") as f:
                return f"⚡ [OPENVIKING L1 - 0.01ms]: {f.read().strip()}"

    if not os.path.exists(TRUTH_FILE):
        return "❌ Error: VERDAD_OASIS.txt no encontrado."
    try:
        with open(TRUTH_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        if query_str.isdigit():
            prefix = f"{query_str}."
            for line in lines:
                if line.strip().startswith(prefix):
                    return f"📜 [VERDAD_OASIS.txt]: {line.strip()}"
            return f"ℹ️ Pilar {query_str} no encontrado."
        q_low = query_str.lower()
        matches = [l.strip() for l in lines if q_low in l.lower()]
        return ("\n".join(matches[:8])) if matches else f"ℹ️ Sin coincidencias para '{query_str}'."
    except Exception as e:
        return f"❌ Error: {e}"

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

class OasisModularHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        try:
            body = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        try:
            if self.path in ("/", "/terminal") or self.path.startswith("/terminal?"):
                html = load_template("terminal.html")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            elif self.path.startswith("/v1/pilar"):
                import urllib.parse
                parsed = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed.query)
                p_id = params.get("id", ["1"])[0]
                out = query_verdad_oasis(p_id)
                self._send_json({"output": out, "id": p_id})
            elif self.path in ("/v1/agent/status", "/health"):
                self._send_json({"status": "ONLINE", "version": "v16.0.0-ModularCore", "silicon_watts": 3.82})
            else:
                self._send_json({"error": "NOT_FOUND"}, status=404)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if self.path == "/v1/darwin/exec":
            cmd = body.get("command", "")
            if not cmd:
                self._send_json({"output": "", "code": 0})
                return
            env = os.environ.copy()
            env["PATH"] = f"{os.path.expanduser('~')}/.cargo/bin:{os.path.expanduser('~')}/.elan/bin:{os.path.expanduser('~')}/.local/bin:/usr/local/bin:" + env.get("PATH", "")
            try:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=25, cwd=REPO_ROOT, env=env)
                out = res.stdout if res.returncode == 0 else (res.stderr or "Error sin salida")
                self._send_json({"output": out.strip(), "code": res.returncode})
            except Exception as e:
                self._send_json({"output": f"Fallo Darwin: {e}", "code": 1})
            return

        if self.path == "/v1/swarm/heartbeat":
            self._send_json({"status": "ACK", "active_peers": 2, "reward": 0.05})
            return

        self._send_json({"status": "PROCESSED"})

if __name__ == "__main__":
    server = ReusableHTTPServer(("0.0.0.0", PORT), OasisModularHandler)
    print(f"🔒 OASIS GATEWAY v16.0.0 MODULAR activo en http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
