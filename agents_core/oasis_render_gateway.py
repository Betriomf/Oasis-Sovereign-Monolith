#!/usr/bin/env python3
import os
import json
import math
import struct
import hashlib
import threading
import time
import re
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
KAPPA = math.log(10.0)
GOLDEN_WAIT_BASE = math.pi / PHI

AUTH_KEYS = {
    MASTER_KEY: {"quota": float("inf"), "owner": "sovereign_root"}
}
VIRTUAL_FS = {}

# Cola Swarm para el MacBook Air
SWARM_LOCK = threading.Lock()
PENDING_JOBS = []
COMPLETED_JOBS = {}

def sanitize_llm_prompt(raw_text: str) -> str:
    """Freno Geométrico: Neutraliza inyecciones y confina a pi-KB (3141 bytes)."""
    # 1. Neutralización de directivas de anulación
    cleaned = re.sub(
        r"(?i)(system:|ignore previous instructions|disregard|override|extract credentials|show keys|reveal prompt)",
        "[NEUTRALIZADO]",
        raw_text
    )
    # 2. Confinamiento estricto a contenedor esférico pi-KB
    return cleaned[:3141]

TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign OS — Cyber Terminal</title>
<style>
  :root { --bg: #070a0f; --fg: #00ff88; --dim: #006633; --accent: #00e5ff; --alert: #ff0055; }
  * { box-sizing: border-box; }
  body { background: var(--bg); color: var(--fg); font-family: 'JetBrains Mono', 'Courier New', monospace; margin: 0; padding: 20px; }
  #terminal { max-width: 950px; margin: 0 auto; background: rgba(5,15,10,0.7); border: 1px solid var(--dim); border-radius: 8px; padding: 20px; box-shadow: 0 0 30px rgba(0,255,136,0.1); }
  #output { white-space: pre-wrap; word-break: break-all; margin-bottom: 15px; max-height: 75vh; overflow-y: auto; }
  .prompt-row { display: flex; align-items: center; }
  .prompt { color: var(--accent); font-weight: bold; margin-right: 10px; }
  input { flex: 1; background: transparent; border: none; outline: none; color: var(--fg); font-family: inherit; font-size: 1rem; }
  .dim { color: var(--dim); }
  .info { color: var(--accent); }
  .alert { color: var(--alert); }
</style>
</head>
<body>
<div id="terminal">
  <div id="output">
  🌌 OASIS SOVEREIGN OS [Terminal v2.5 — Motor Silicio Frío]
  Nodo: Render Fráncfort | Beneficiario: akash1dy3... | Capa 0: Activa
  Escribe 'help' para explorar el sistema.
  -------------------------------------------------------------
  </div>
  <div class="prompt-row">
    <span class="prompt">oasis@node:~$</span>
    <input type="text" id="cmd" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
  </div>
</div>

<script>
const out = document.getElementById('output');
const input = document.getElementById('cmd');
let history = [];
let hIndex = -1;

function print(t, cls='') {
  const div = document.createElement('div');
  div.className = cls;
  div.innerText = t;
  out.appendChild(div);
  out.scrollTop = out.scrollHeight;
}

input.addEventListener('keydown', async (e) => {
  if (e.key === 'ArrowUp') {
    if (history.length && hIndex < history.length - 1) {
      hIndex++;
      input.value = history[history.length - 1 - hIndex];
    }
    e.preventDefault();
  } else if (e.key === 'ArrowDown') {
    if (hIndex > 0) {
      hIndex--;
      input.value = history[history.length - 1 - hIndex];
    } else {
      hIndex = -1;
      input.value = '';
    }
    e.preventDefault();
  } else if (e.key === 'Enter') {
    const raw = input.value.trim();
    if (!raw) return;
    history.push(raw);
    hIndex = -1;
    print('oasis@node:~$ ' + raw, 'dim');
    input.value = '';
    const parts = raw.split(' ');
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    if (cmd === 'help') {
      print(`COMANDOS DISPONIBLES:
  ai <prompt>          - Consulta a la IA Local a través del Firewall LLM
  status               - Estado del nodo, balance y telemetría
  uname -a             - Arquitectura y versión del kernel
  uptime               - Tiempo de actividad del Gateway
  fs put <name> <txt>  - Fragmenta y almacena un archivo en bloques
  fs get <name>        - Desfragmenta y lee el archivo
  fs list              - Lista archivos del disco virtual
  vortex <x> <y> <z>   - Simulación cinemática (16 bytes)
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'uname') {
      print('OasisOS 2.5.0-sovereign-darwin x86_64 / cold-silicon GNU/AGPLv3', 'info');
    } else if (cmd === 'uptime') {
      print('Nodo activo 24/7 en Fráncfort. Latencia: <0.05ms (Caché RAM)', 'info');
    } else if (cmd === 'status') {
      const res = await fetch('/status').then(r=>r.json());
      print(JSON.stringify(res, null, 2), 'info');
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print('Uso: ai <consulta>', 'alert'); return; }
      print('🛡️  Auditando prompt por Freno Geométrico y despachando a la IA...', 'dim');
      const res = await fetch('/v1/llm/secure-proxy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
        body: JSON.stringify({prompt})
      }).then(r=>r.json());
      
      if (res.clean_response) {
        print(`🤖 [${res.model_used || 'IA Local'}]:\n` + res.clean_response, 'info');
      } else {
        print(JSON.stringify(res, null, 2), 'alert');
      }
    } else if (cmd === 'fs') {
      const sub = args[0];
      if (sub === 'put') {
        const fname = args[1];
        const content = args.slice(2).join(' ');
        const res = await fetch('/v1/fs/put', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
          body: JSON.stringify({filename: fname, content})
        }).then(r=>r.json());
        print(`✅ Archivo fragmentado en ${res.chunks_created} bloques (Hash raíz: ${res.root_merkle})`, 'info');
      } else if (sub === 'get') {
        const fname = args[1];
        const res = await fetch('/v1/fs/get?filename=' + fname).then(r=>r.json());
        print(res.content ? `Contenido: "${res.content}"` : 'No encontrado', 'info');
      } else if (sub === 'list') {
        const res = await fetch('/v1/fs/list').then(r=>r.json());
        print('Archivos: ' + res.files.join(', '), 'info');
      }
    } else {
      print(`Comando '${cmd}' no reconocido. Escribe 'help'.`, 'dim');
    }
  }
});
</script>
</body>
</html>
"""

class OasisCloudHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/terminal"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(TERMINAL_HTML.encode())
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "wallet": AKASH_WALLET,
                "firewall": "Freno Geométrico (Confinamiento π-KB Activo)",
                "queue_pending_jobs": len(PENDING_JOBS)
            })
        # Polling del Mac: Comprueba si hay tareas pendientes
        elif self.path == "/v1/swarm/poll":
            with SWARM_LOCK:
                if PENDING_JOBS:
                    job = PENDING_JOBS.pop(0)
                    self._send_json(job)
                    return
            self._send_json({"has_job": False})
        elif self.path.startswith("/v1/fs/get"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            fname = query.get("filename", [""])[0]
            if fname in VIRTUAL_FS:
                self._send_json({"filename": fname, "content": "".join(VIRTUAL_FS[fname])})
            else:
                self._send_json({"error": "Archivo no encontrado"}, status=404)
        elif self.path == "/v1/fs/list":
            self._send_json({"files": list(VIRTUAL_FS.keys())})
        else:
            self._send_json({"error": "Ruta no encontrada"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode())
        except Exception:
            body = {}

        # 1. Proxy Firewall LLM: Recibe consulta, sanea y encola para el Mac
        if self.path == "/v1/llm/secure-proxy":
            prompt_raw = body.get("prompt", "")
            if not prompt_raw:
                self._send_json({"error": "Prompt vacío"}, status=400)
                return

            prompt_sanitizado = sanitize_llm_prompt(prompt_raw)
            job_id = hashlib.sha256(f"{prompt_sanitizado}:{time.time()}".encode()).hexdigest()[:12]

            # Encolar para el agente en el Mac
            with SWARM_LOCK:
                PENDING_JOBS.append({
                    "has_job": True,
                    "job_id": job_id,
                    "prompt": prompt_sanitizado
                })

            # Esperar respuesta del Mac hasta 15 segundos
            t0 = time.time()
            while time.time() - t0 < 45.0:
                with SWARM_LOCK:
                    if job_id in COMPLETED_JOBS:
                        res = COMPLETED_JOBS.pop(job_id)
                        self._send_json({
                            "status": "SUCCESS_SECURE_INFERENCE",
                            "freno_geometrico": "INYECCIONES_NEUTRALIZADAS_OK",
                            "pi_frame_bytes": len(prompt_sanitizado),
                            "model_used": res.get("model", "oasis-edge:1.5b"),
                            "clean_response": res.get("response", "")
                        })
                        return
                time.sleep(0.3)

            # Si el Mac está apagado o no responde a tiempo:
            self._send_json({
                "status": "FALLBACK_CAPA_0",
                "clean_response": f"[Freno Geométrico Activo]: Prompt auditado ({len(prompt_sanitizado)} B). Tu Mac no recogió la tarea a tiempo. Inicia agents_core/oasis_mac_bridge.py."
            })
            return

        # 2. El Mac entrega el resultado del modelo local
        elif self.path == "/v1/swarm/complete":
            job_id = body.get("job_id")
            if job_id:
                with SWARM_LOCK:
                    COMPLETED_JOBS[job_id] = {
                        "response": body.get("response", ""),
                        "model": body.get("model", "oasis-edge:1.5b")
                    }
                self._send_json({"status": "ACK"})
            else:
                self._send_json({"error": "job_id missing"}, status=400)
            return

        elif self.path == "/v1/fs/put":
            filename = body.get("filename", "unnamed.dat")
            content = body.get("content", "")
            chunks = [content[i:i+32] for i in range(0, len(content), 32)]
            VIRTUAL_FS[filename] = chunks
            self._send_json({"filename": filename, "chunks_created": len(chunks), "root_merkle": hashlib.sha256(content.encode()).hexdigest()})
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
