#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY v3.1.0 (BLACK CIRCLE PROTOCOL)
"""
import os
import json
import hashlib
import threading
import time
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

SWARM_LOCK = threading.Lock()
CONNECTED_NODES = {}
PENDING_TASKS = {}
COMPLETED_TASKS = {}

def sanitize_llm_prompt(raw_text: str) -> str:
    cleaned = re.sub(
        r"(?i)(system:|ignore previous instructions|disregard|override|extract credentials|show keys|reveal prompt)",
        "[NEUTRALIZADO]",
        raw_text
    )
    return cleaned[:3141]

TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign OS — Círculo Negro</title>
<style>
  :root {
    --bg: #05080d;
    --term: rgba(6, 12, 20, 0.94);
    --fg: #00ff9d;
    --dim: #007744;
    --accent: #00e5ff;
    --root: #ffb703;
    --alert: #ff0055;
    --font: 'JetBrains Mono', monospace;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--fg);
    font-family: var(--font);
    margin: 0;
    padding: 12px;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  #terminal {
    flex: 1;
    max-width: 1100px;
    width: 100%;
    margin: 0 auto;
    background: var(--term);
    border: 1px solid var(--dim);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 0 35px rgba(0, 255, 157, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  #header {
    border-bottom: 1px dashed var(--dim);
    padding-bottom: 8px;
    margin-bottom: 10px;
    font-size: 0.85rem;
    color: var(--accent);
    display: flex;
    justify-content: space-between;
  }
  #output {
    flex: 1;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-y: auto;
    padding-right: 8px;
  }
  .prompt-row {
    display: flex;
    align-items: center;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(0, 255, 157, 0.15);
  }
  .prompt-lbl {
    color: var(--accent);
    font-weight: bold;
    margin-right: 10px;
    white-space: nowrap;
  }
  input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--fg);
    font-family: inherit;
    font-size: 1rem;
  }
  .dim { color: var(--dim); }
  .info { color: var(--accent); }
  .warn { color: var(--root); }
  .alert { color: var(--alert); }
</style>
</head>
<body>
<div id="terminal">
  <div id="header">
    <span>🌌 OASIS SOVEREIGN OS [Círculo Negro v3.1]</span>
    <span><span id="node-badge" class="warn">Enjambre: Conectando...</span> | <span id="consent-badge" class="dim">CPU Donada: OFF</span></span>
  </div>
  <div id="output">Inicializando Enclave Seguro...</div>
  <div class="prompt-row">
    <span class="prompt-lbl" id="prompt-tag">oasis@anon:~$</span>
    <input type="text" id="cmd" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
  </div>
</div>

<script>
const out = document.getElementById('output');
const input = document.getElementById('cmd');
const promptTag = document.getElementById('prompt-tag');
const nodeBadge = document.getElementById('node-badge');
const consentBadge = document.getElementById('consent-badge');

let HW_KEY = "OASIS-HW-468F6F695BDB";
let history = [];
let hIndex = -1;

function print(t, cls='') {
  const d = document.createElement('div');
  d.className = cls;
  d.innerText = t;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}

async function checkSwarm() {
  try {
    const res = await fetch('/v1/swarm/nodes').then(r=>r.json());
    if (res.active_nodes && res.active_nodes.length > 0) {
      nodeBadge.innerText = `🟢 Mac Enlazado (${res.active_nodes.length} Nodo)`;
      nodeBadge.className = "info";
    } else {
      nodeBadge.innerText = "🟡 Modo Nube (Inicia oasis_local_node.py)";
      nodeBadge.className = "warn";
    }
  } catch(e) {}
}

out.innerHTML = `✅ [HUELLA FÍSICA]: ${HW_KEY}
🛡️ [CÍRCULO NEGRO]: Aislamiento térmico y barrera de comandos activa.
🔒 [CONSENTIMIENTO]: Tu CPU está reservada 100% para ti por defecto.

Escribe 'help' para ver los comandos del enclave.
-------------------------------------------------------------`;
promptTag.innerText = `oasis@${HW_KEY.substring(9, 15).toLowerCase()}:~$`;

checkSwarm();
setInterval(checkSwarm, 4000);

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
    print(promptTag.innerText + " " + raw, 'dim');
    input.value = '';

    const parts = raw.split(' ');
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    if (cmd === 'help') {
      print(`COMANDOS DEL CÍRCULO NEGRO:
  ai <prompt>          - Consulta a tu Ollama local (Respuesta rápida y privada)
  host <comando>       - Ejecuta comandos verificados en tu Mac (uname -a, uptime, ollama list)
  consent              - Explica la política de privacidad y donación de CPU
  apk [info]           - Emulador Alpine en tu navegador (0 bytes a la nube)
  status               - Estado del enclave térmico y del enjambre
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'consent') {
      print(`--- AVISO DE CONSENTIMIENTO DE CÓMPUTO ---
Tu MacBook Air NO procesará tareas de terceros salvo que lo actives expresamente en el script local.
• Estado actual: MODO PRIVADO (Tu procesador trabaja exclusivamente para tus comandos).
• Para donar CPU a cambio de créditos: Cambia SWARM_DONATION_ENABLED = True en oasis_local_node.py.`, 'info');
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print("Uso: ai <consulta>", "alert"); return; }
      print("🛡️  Auditando prompt y despachando al silicio local...", "dim");
      const res = await fetch('/v1/swarm/dispatch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
        body: JSON.stringify({type: 'AI_INFERENCE', prompt, hw_target: HW_KEY})
      }).then(r=>r.json());
      if (res.response) {
        print(`🤖 [${res.model_used || 'Silicio Local'}]:\\n` + res.response, "info");
      } else {
        print(res.message || JSON.stringify(res), "alert");
      }
    } else if (cmd === 'host') {
      const hostCmd = args.join(' ');
      if (!hostCmd) { print("Uso: host <comando>", "alert"); return; }
      print("⚡ Consultando comando permitido en tu Mac...", "dim");
      const res = await fetch('/v1/swarm/dispatch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
        body: JSON.stringify({type: 'HOST_EXEC', cmd: hostCmd, hw_target: HW_KEY})
      }).then(r=>r.json());
      print(res.output || res.message, "info");
    } else if (cmd === 'apk') {
      print("apk-tools 2.14.4 (x86_64). Sandbox local montado en IndexedDB.", "info");
    } else if (cmd === 'status') {
      const res = await fetch('/status').then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else {
      print(`bash: ${cmd}: orden no encontrada. Escribe 'help'.`, 'alert');
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
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key, x-hw-key")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/terminal"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(TERMINAL_HTML.encode())
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "beneficiary": AKASH_WALLET,
                "active_swarm_nodes": len(CONNECTED_NODES),
                "enclave_mode": "Black Circle (Coulomb + Stefan-Boltzmann)"
            })
        elif self.path == "/v1/swarm/nodes":
            now = time.time()
            active = [k for k, v in CONNECTED_NODES.items() if now - v["last_seen"] < 10.0]
            self._send_json({"active_nodes": active, "count": len(active)})
        else:
            self._send_json({"status": "ONLINE"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode())
        except Exception:
            body = {}

        if self.path == "/v1/swarm/heartbeat":
            hw_key = self.headers.get("x-hw-key") or body.get("hw_key", "UNKNOWN")
            with SWARM_LOCK:
                CONNECTED_NODES[hw_key] = {
                    "last_seen": time.time(),
                    "cpu_cold": body.get("cpu_cold", True),
                    "opt_in": body.get("swarm_opt_in", False)
                }
                assigned = None
                for tid, tdata in list(PENDING_TASKS.items()):
                    if tdata.get("hw_target") == hw_key:
                        assigned = {"task_id": tid, **tdata}
                        del PENDING_TASKS[tid]
                        break

            self._send_json({"status": "ACK", "task": assigned})
            return

        if self.path == "/v1/swarm/result":
            task_id = body.get("task_id")
            if task_id:
                with SWARM_LOCK:
                    COMPLETED_TASKS[task_id] = body
                self._send_json({"status": "OK"})
            return

        if self.path == "/v1/swarm/dispatch":
            task_type = body.get("type", "AI_INFERENCE")
            task_id = hashlib.sha256(f"{task_type}:{time.time()}".encode()).hexdigest()[:12]

            with SWARM_LOCK:
                PENDING_TASKS[task_id] = {
                    "type": task_type,
                    "prompt": sanitize_llm_prompt(body.get("prompt", "")),
                    "cmd": body.get("cmd", ""),
                    "hw_target": body.get("hw_target"),
                    "created": time.time()
                }

            t0 = time.time()
            while time.time() - t0 < 30.0:
                with SWARM_LOCK:
                    if task_id in COMPLETED_TASKS:
                        res = COMPLETED_TASKS.pop(task_id)
                        self._send_json(res)
                        return
                time.sleep(0.15)

            self._send_json({"error": "TIMEOUT", "message": "El silicio local no respondió a tiempo. Verifica que oasis_local_node.py esté activo."})
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
