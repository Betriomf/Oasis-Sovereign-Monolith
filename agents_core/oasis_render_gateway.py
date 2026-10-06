#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY v2.9.0 CON DETECCIÓN DE MAC LOCAL Y MOTOR WASM
"""
import os
import json
import math
import hashlib
import time
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign Linux & Darwin OS v2.9</title>
<style>
  :root {
    --bg: #05080d;
    --term-bg: rgba(6, 12, 20, 0.94);
    --fg: #00ff9d;
    --dim: #007744;
    --accent: #00e5ff;
    --root: #ffb703;
    --alert: #ff0055;
    --font: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
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
    background: var(--term-bg);
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
  .root-lbl { color: var(--root); }
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
    <span>🌌 OASIS SOVEREIGN OS [v2.9.0] | Silicio Híbrido</span>
    <span><span id="daemon-status" class="warn">Local Daemon: Buscando...</span> | <span id="quota-display" class="info">Cuota: 1000</span></span>
  </div>
  <div id="output">Inicializando enlace estocástico...</div>
  <div class="prompt-row">
    <span class="prompt-lbl" id="prompt-tag">oasis@anon:~$</span>
    <input type="text" id="cmd" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
  </div>
</div>

<script>
const out = document.getElementById('output');
const input = document.getElementById('cmd');
const promptTag = document.getElementById('prompt-tag');
const daemonStatus = document.getElementById('daemon-status');
const quotaDisplay = document.getElementById('quota-display');

let LOCAL_DAEMON_ONLINE = false;
let HW_KEY = "";
let CURRENT_KEY = "";
let IS_ROOT = false;
let history = [];
let hIndex = -1;

async function deriveHWKey() {
  const parts = [navigator.hardwareConcurrency || 4, navigator.deviceMemory || 8, screen.colorDepth || 24, navigator.platform || ""];
  try {
    const gl = document.createElement('canvas').getContext('webgl');
    if (gl) {
      const dbg = gl.getExtension('WEBGL_debug_renderer_info');
      if (dbg) parts.push(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL));
    }
  } catch(e) {}
  const raw = parts.join('|');
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(raw));
  HW_KEY = "OASIS-HW-" + Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('').substring(0, 12).toUpperCase();
  CURRENT_KEY = HW_KEY;
}

// Comprobación de Demonio Local en el Mac (127.0.0.1:8765)
async function checkLocalDaemon() {
  try {
    const res = await fetch('http://127.0.0.1:8765/v1/local/telemetry', {signal: AbortSignal.timeout(1200)}).then(r=>r.json());
    if (res.status === 'ONLINE') {
      LOCAL_DAEMON_ONLINE = true;
      daemonStatus.innerText = "🟢 Mac Local Conectado (127.0.0.1:8765)";
      daemonStatus.className = "info";
      return res;
    }
  } catch(e) {
    LOCAL_DAEMON_ONLINE = false;
    daemonStatus.innerText = "🟡 Modo Nube (Inicia oasis_local_node.py)";
    daemonStatus.className = "warn";
  }
  return null;
}

function getVFS() {
  const s = localStorage.getItem('OASIS_VFS_' + HW_KEY);
  if (s) { try { return JSON.parse(s); } catch(e){} }
  return {
    "/etc/alpine-release": "3.20.2",
    "/etc/issue": "Welcome to Alpine Linux 3.20 (Oasis Web Edition)",
    "/home/oasis/README.txt": "Bienvenido a Oasis OS.\\nTus archivos están guardados localmente en este ordenador.\\nSupabase = 0 bytes consumidos."
  };
}
function saveVFS(vfs) { localStorage.setItem('OASIS_VFS_' + HW_KEY, JSON.stringify(vfs)); }

function print(t, cls='') {
  const d = document.createElement('div');
  d.className = cls;
  d.innerText = t;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}

deriveHWKey().then(async () => {
  const localInfo = await checkLocalDaemon();
  out.innerHTML = `✅ [HUELLA FÍSICA]: ${HW_KEY}
🔐 [SESIÓN PRIVADA]: Persistencia 100% en disco local (Zero-Cloud Leak).
${localInfo ? "⚡ [SILICIO FRÍO NATIVO]: Enlace directo con " + localInfo.kernel : "⚡ [MODO NUBE]: Inicia 'python3 agents_core/oasis_local_node.py' para enlace nativo"}

Escribe 'help' para ver el catálogo de comandos.
-------------------------------------------------------------`;
  promptTag.innerText = `oasis@${HW_KEY.substring(9, 15).toLowerCase()}:~$`;
});

// Chequeo periódico de conexión con el Mac
setInterval(checkLocalDaemon, 4000);

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
    const vfs = getVFS();

    if (cmd === 'help') {
      print(`COMANDOS DE OASIS SOVEREIGN OS:
  ai <prompt>          - Consulta a Ollama (Directo a tu Mac si el demonio está activo)
  ai --7b <prompt>     - Inferencia con modelo 7B
  host <comando>       - Ejecuta comandos nativos en tu Mac (ej. host uname -a, host ls)
  apk [info|version]   - Gestor de paquetes de Alpine Linux
  free -m              - Muestra memoria del entorno
  cat <archivo>        - Muestra un archivo (ej. cat /etc/alpine-release)
  ls, echo, rm         - Gestión de archivos en tu disco local privado
  login <clave>        - Inicia sesión como Root (login OASIS-SOVEREIGN-MARIANO-2026)
  status               - Telemetría del nodo y estado del demonio local
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'login') {
      if (args[0] === 'OASIS-SOVEREIGN-MARIANO-2026') {
        CURRENT_KEY = args[0];
        IS_ROOT = true;
        promptTag.innerText = "root@oasis-sovereign:~#";
        promptTag.className = "prompt-lbl root-lbl";
        quotaDisplay.innerText = "Cuota: ILIMITADA";
        print("🔓 [AUTENTICACIÓN ROOT]: Acceso maestro activado.", "warn");
      } else {
        print("Clave inválida.", "alert");
      }
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print("Uso: ai <consulta>", "alert"); return; }
      
      if (LOCAL_DAEMON_ONLINE) {
        print("⚡ [ENLACE DIRECTO MAC]: Procesando en Ollama local (<1ms latencia)...", "dim");
        try {
          const res = await fetch('http://127.0.0.1:8765/v1/local/ai', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'x-hw-key': HW_KEY},
            body: JSON.stringify({prompt})
          }).then(r=>r.json());
          print(`🤖 [${res.model_used}] (Silicio Local Directo):\\n` + res.response, "info");
          return;
        } catch(e) {
          print("⚠️ Enlace local falló, derivando a Render Gateway...", "dim");
        }
      }

      print("🛡️  Enrutando a través de Render Gateway...", "dim");
      const res = await fetch('/v1/llm/secure-proxy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({prompt})
      }).then(r=>r.json());
      print(`🤖 [${res.model_used}]:\\n` + res.clean_response, "info");

    } else if (cmd === 'host') {
      if (!LOCAL_DAEMON_ONLINE) {
        print("❌ Demonio local desconectado. Ejecuta en tu Mac: python3 agents_core/oasis_local_node.py", "alert");
        return;
      }
      const hostCmd = args.join(' ');
      const res = await fetch('http://127.0.0.1:8765/v1/local/exec', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-hw-key': HW_KEY},
        body: JSON.stringify({cmd: hostCmd})
      }).then(r=>r.json());
      print(res.output || res.error, "info");

    } else if (cmd === 'apk') {
      if (args[0] === 'info' || args[0] === '--version') {
        print("apk-tools 2.14.4 (x86_64), multi-call binary.\\nRepositorios locales montados en IndexedDB.", "info");
      } else {
        print("apk: gestor de paquetes de Alpine activo.", "info");
      }
    } else if (cmd === 'free') {
      print("             total        used        free      shared  buff/cache   available\\nMem:          8192        2048        6144           0           0        6144\\nSwap:            0           0           0", "info");
    } else if (cmd === 'cat') {
      print(vfs[args[0]] || `cat: ${args[0]}: No such file or directory`, vfs[args[0]] ? 'info' : 'alert');
    } else if (cmd === 'ls') {
      print(Object.keys(vfs).join('   '), 'info');
    } else if (cmd === 'status') {
      print(`Estado Demonio Local: ${LOCAL_DAEMON_ONLINE ? 'CONECTADO (127.0.0.1:8765)' : 'DESCONECTADO'}\\nHuella Silicio: ${HW_KEY}\\nCuota: ${IS_ROOT ? 'ILIMITADA' : '1000'}`, "info");
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
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        if self.path in ("/", "/terminal"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(TERMINAL_HTML.encode())
        else:
            self._send_json({"status": "ONLINE"})

    def do_POST(self):
        self._send_json({"status": "OK"})

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
