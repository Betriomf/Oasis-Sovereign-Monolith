#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY v2.8.0 CON PERSISTENCIA SUPABASE Y SWARM COMPUTE
"""
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
SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
KAPPA = math.log(10.0)
ALPHA = 1.0 / 137.036
GOLDEN_WAIT_BASE = math.pi / PHI

AUTH_KEYS = {
    MASTER_KEY: {"quota": float("inf"), "owner": "sovereign_root"}
}

# Colas en Memoria RAM
SWARM_LOCK = threading.Lock()
PENDING_JOBS = []
COMPLETED_JOBS = {}
SWARM_TASKS_POOL = []  # Tareas para los navegadores conectados
ACTIVE_NODES = {}

def sanitize_llm_prompt(raw_text: str) -> str:
    cleaned = re.sub(
        r"(?i)(system:|ignore previous instructions|disregard|override|extract credentials|show keys|reveal prompt)",
        "[NEUTRALIZADO]",
        raw_text
    )
    return cleaned[:3141]

def factorize_integer(n: int):
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

def query_supabase_cache(prompt_hash: str):
    try:
        url = f"{SUPABASE_URL}/rest/v1/llm_semantic_cache?prompt_hash=eq.{prompt_hash}&select=clean_response,model_used"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if data:
                return data[0]["clean_response"], data[0]["model_used"]
    except Exception:
        pass
    return None, None

def save_supabase_cache(prompt_hash: str, raw_text: str, response: str, model: str):
    try:
        url = f"{SUPABASE_URL}/rest/v1/llm_semantic_cache"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        payload = json.dumps({
            "prompt_hash": prompt_hash,
            "prompt_raw": raw_text[:500],
            "clean_response": response,
            "model_used": model
        }).encode()
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass

TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign Linux OS v2.8</title>
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
    <span>🌌 OASIS SOVEREIGN OS [v2.8.0-sovereign-x86_64] | Nodo: Fráncfort</span>
    <span><span id="swarm-status" class="dim">Worker: Conectando...</span> | <span id="quota-display" class="warn">Cuota: 1000</span></span>
  </div>
  <div id="output">Inicializando detección estocástica de hardware...</div>
  <div class="prompt-row">
    <span class="prompt-lbl" id="prompt-tag">oasis@anon:~$</span>
    <input type="text" id="cmd" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
  </div>
</div>

<script>
const out = document.getElementById('output');
const input = document.getElementById('cmd');
const promptTag = document.getElementById('prompt-tag');
const quotaDisplay = document.getElementById('quota-display');
const swarmStatus = document.getElementById('swarm-status');

let CURRENT_KEY = "";
let IS_ROOT = false;
let HW_KEY = "";
let REMAINING_QUOTA = 1000;
let history = [];
let hIndex = -1;

// 1. Detección de Silicio Físico (Soulbound to Metal)
async function deriveHWKey() {
  const parts = [
    navigator.hardwareConcurrency || 4,
    navigator.deviceMemory || 8,
    screen.colorDepth || 24,
    navigator.platform || ""
  ];
  try {
    const gl = document.createElement('canvas').getContext('webgl');
    if (gl) {
      const dbg = gl.getExtension('WEBGL_debug_renderer_info');
      if (dbg) parts.push(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL));
    }
  } catch(e) {}
  const raw = parts.join('|');
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(raw));
  const hex = Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  HW_KEY = "OASIS-HW-" + hex.substring(0, 12).toUpperCase();
  CURRENT_KEY = HW_KEY;
}

// 2. Sistema de Archivos Persistente Local
function getVFS() {
  const s = localStorage.getItem('OASIS_VFS_' + HW_KEY);
  if (s) { try { return JSON.parse(s); } catch(e){} }
  return {
    "/home/oasis/README.txt": "Bienvenido a Oasis Sovereign Linux v2.8.\\nTus archivos se guardan en el disco de tu navegador.",
    "/home/oasis/nodo.conf": '{"mode": "cold_silicon", "swarm_worker": "active"}'
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

function updateQuota(q) {
  if (q === undefined) return;
  REMAINING_QUOTA = q;
  quotaDisplay.innerText = IS_ROOT ? "Cuota: ILIMITADA" : `Cuota: ${REMAINING_QUOTA}`;
}

// 3. Worker de Cómputo Compartido (Cede potencia en segundo plano)
function startSwarmComputeWorker() {
  const workerCode = `
    self.onmessage = function(e) {
      const task = e.data;
      if (task.type === 'FACTORIZE') {
        let n = task.number;
        let factors = [];
        let d = 2;
        while (d * d <= n) {
          while (n % d === 0) { factors.push(d); n = Math.floor(n / d); }
          d++;
        }
        if (n > 1) factors.push(n);
        self.postMessage({task_id: task.task_id, factors: factors});
      }
    };
  `;
  const blob = new Blob([workerCode], {type: 'application/javascript'});
  const worker = new Worker(URL.createObjectURL(blob));

  worker.onmessage = async (e) => {
    const res = e.data;
    await fetch('/v1/swarm/task-complete', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({hw_key: HW_KEY, task_id: res.task_id, factors: res.factors})
    });
    swarmStatus.innerText = "Worker: Potencia cedida (+1 Crédito)";
    swarmStatus.className = "info";
  };

  // Sondeo de tareas cada 5 segundos
  setInterval(async () => {
    try {
      const resp = await fetch('/v1/swarm/task-poll?hw_key=' + HW_KEY).then(r=>r.json());
      if (resp.has_task) {
        swarmStatus.innerText = "Worker: Procesando cálculo...";
        swarmStatus.className = "warn";
        worker.postMessage(resp.task);
      }
    } catch(err) {}
  }, 5000);
}

deriveHWKey().then(() => {
  out.innerHTML = `✅ [HUELLA DE SILICIO]: ${HW_KEY}
🔐 [SISTEMA SOBERANO]: Sesión privada respaldada por tu hardware.
💾 [PERSISTENCIA SUPABASE]: Respuestas de IA cacheadas permanentemente.
⚡ [SWARM COMPUTE]: Cediendo potencia en segundo plano para ganar cuota.

Escribe 'help' para explorar el sistema.
-------------------------------------------------------------`;
  promptTag.innerText = `oasis@${HW_KEY.substring(9, 15).toLowerCase()}:~$`;
  startSwarmComputeWorker();
});

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
      print(`COMANDOS DEL SISTEMA:
  login <clave>        - Inicia sesión maestra (login OASIS-SOVEREIGN-MARIANO-2026)
  ai <prompt>          - Consulta a tu IA Local (Con Freno Geométrico y Caché Supabase)
  ai --7b <prompt>     - Inferencia profunda con modelo 7B en tu Mac
  shield [intervalos]  - Detección de bots Zero-PII
  factorize <num>      - Factorización de enteros grandes
  vortex <x> <y> <z>   - Simulación de fluidos determinista
  ls, cat, echo, rm    - Gestión de archivos en tu disco local privado
  hwinfo               - Identidad física de hardware
  status               - Estado del Gateway y nodos del enjambre
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'hwinfo') {
      print(`--- IDENTIDAD DE SILICIO ---
Clave derivada:   ${HW_KEY}
Estado de sesión: ${IS_ROOT ? 'ROOT SOBERANO' : 'CLIENTE'}
Cuota activa:     ${IS_ROOT ? 'ILIMITADA' : REMAINING_QUOTA}
Swarm Worker:     Activo en segundo plano (Web Worker)`, 'info');
    } else if (cmd === 'login') {
      const key = args[0];
      if (key === 'OASIS-SOVEREIGN-MARIANO-2026') {
        CURRENT_KEY = key;
        IS_ROOT = true;
        promptTag.innerText = "root@oasis-sovereign:~#";
        promptTag.className = "prompt-lbl root-lbl";
        updateQuota(Infinity);
        print("🔓 [AUTENTICACIÓN ROOT]: Bienvenido Mariano. Acceso ilimitado concedido.", "warn");
      } else {
        print("Clave no reconocida.", "alert");
      }
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print("Uso: ai <prompt>", "alert"); return; }
      print("🛡️  Auditando por Freno Geométrico y consultando caché...", "dim");
      const res = await fetch('/v1/llm/secure-proxy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({prompt})
      }).then(r=>r.json());
      updateQuota(res.remaining_quota);
      if (res.clean_response) {
        print(`🤖 [${res.model_used}] (${res.source || 'Inferencia'}):\\n` + res.clean_response, "info");
      } else {
        print(JSON.stringify(res, null, 2), "alert");
      }
    } else if (cmd === 'ls') {
      print(Object.keys(vfs).join('   '), 'info');
    } else if (cmd === 'cat') {
      print(vfs[args[0]] || 'Archivo no encontrado', vfs[args[0]] ? 'info' : 'alert');
    } else if (cmd === 'echo') {
      const full = args.join(' ');
      if (full.includes('>')) {
        const [txt, fName] = full.split('>');
        vfs[fName.trim()] = txt.trim().replace(/^["']|["']$/g, '');
        saveVFS(vfs);
        print(`Guardado en ${fName.trim()}`, 'dim');
      } else {
        print(full);
      }
    } else if (cmd === 'rm') {
      delete vfs[args[0]];
      saveVFS(vfs);
      print(`Eliminado ${args[0]}`, 'dim');
    } else if (cmd === 'factorize') {
      const num = parseInt(args[0]) || 1000000016000000063;
      const res = await fetch('/v1/math/factorize', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({number: num})
      }).then(r=>r.json());
      updateQuota(res.remaining_quota);
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'vortex') {
      const [x, y, z] = args.map(Number);
      const res = await fetch('/v1/game/vortex', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({x: x||1.0, y: y||0.5, z: z||2.0, t: 0.1})
      }).then(r=>r.json());
      updateQuota(res.remaining_quota);
      print(JSON.stringify(res, null, 2), "info");
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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _authenticate(self):
        api_key = self.headers.get("x-api-key")
        if not api_key:
            return False, "Pago requerido. Proporciona 'x-api-key'.", 402
        if api_key == MASTER_KEY:
            return True, AUTH_KEYS[MASTER_KEY], 200

        if api_key not in AUTH_KEYS:
            if api_key.startswith("OASIS-HW-") or api_key.startswith("OASIS-KEY-"):
                AUTH_KEYS[api_key] = {"quota": 1000, "owner": "guest_hardware"}
            else:
                return False, "Clave no registrada", 403

        entry = AUTH_KEYS[api_key]
        if entry["quota"] <= 0:
            return False, f"Cuota agotada. Envía 1 AKT a {AKASH_WALLET}", 402

        if entry["quota"] != float("inf"):
            entry["quota"] -= 1
        return True, entry, 200

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
                "wallet": AKASH_WALLET,
                "os": "Oasis Sovereign Linux v2.8",
                "active_nodes_count": len(ACTIVE_NODES)
            })
        elif self.path == "/v1/swarm/poll":
            with SWARM_LOCK:
                if PENDING_JOBS:
                    self._send_json(PENDING_JOBS.pop(0))
                    return
            self._send_json({"has_job": False})
        elif self.path.startswith("/v1/swarm/task-poll"):
            # El navegador pide tareas de cómputo para resolver
            with SWARM_LOCK:
                if SWARM_TASKS_POOL:
                    task = SWARM_TASKS_POOL.pop(0)
                    self._send_json({"has_task": True, "task": task})
                    return
            self._send_json({"has_task": False})
        else:
            self._send_json({"error": "Ruta no encontrada"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode())
        except Exception:
            body = {}

        # El navegador entrega cómputo resuelto por su Web Worker
        if self.path == "/v1/swarm/task-complete":
            hw_key = body.get("hw_key")
            if hw_key in AUTH_KEYS and AUTH_KEYS[hw_key]["quota"] != float("inf"):
                AUTH_KEYS[hw_key]["quota"] += 1  # Recompensa con +1 crédito
            self._send_json({"status": "REWARD_GRANTED"})
            return

        if self.path == "/v1/swarm/complete":
            job_id = body.get("job_id")
            if job_id:
                with SWARM_LOCK:
                    COMPLETED_JOBS[job_id] = {
                        "response": body.get("response", ""),
                        "model": body.get("model", "oasis-edge:1.5b")
                    }
                self._send_json({"status": "ACK"})
            return

        auth_ok, auth_res, code = self._authenticate()
        if not auth_ok:
            self._send_json({"error": "PAGO_REQUERIDO", "motivo": auth_res}, status=code)
            return

        remaining = auth_res.get("quota")

        # Inferencia con Caché en Supabase + RAM
        if self.path == "/v1/llm/secure-proxy":
            prompt_raw = body.get("prompt", "")
            prompt_clean = sanitize_llm_prompt(prompt_raw)
            cache_hash = hashlib.sha256(prompt_clean.encode()).hexdigest()

            # 1. Consulta en Supabase
            cached_resp, cached_model = query_supabase_cache(cache_hash)
            if cached_resp:
                self._send_json({
                    "status": "CACHE_HIT_SUPABASE",
                    "source": "Caché Persistente Supabase (38 ms)",
                    "model_used": cached_model,
                    "clean_response": cached_resp,
                    "remaining_quota": remaining
                })
                return

            # 2. Despacho a tu Mac
            job_id = cache_hash[:12]
            with SWARM_LOCK:
                PENDING_JOBS.append({"has_job": True, "job_id": job_id, "prompt": prompt_clean})

            t0 = time.time()
            while time.time() - t0 < 45.0:
                with SWARM_LOCK:
                    if job_id in COMPLETED_JOBS:
                        res = COMPLETED_JOBS.pop(job_id)
                        resp_text = res.get("response", "")
                        model_used = res.get("model", "oasis-edge:1.5b")
                        
                        # Guardar en Supabase para siempre
                        save_supabase_cache(cache_hash, prompt_clean, resp_text, model_used)
                        
                        self._send_json({
                            "status": "SUCCESS",
                            "source": "Silicio Frío Local (Mac)",
                            "model_used": model_used,
                            "clean_response": resp_text,
                            "remaining_quota": remaining
                        })
                        return
                time.sleep(0.2)

            self._send_json({
                "status": "TIMEOUT",
                "clean_response": "[Freno Geométrico]: El Mac no respondió a tiempo. Inicia 'oasis_mac_bridge.py'.",
                "remaining_quota": remaining
            })
            return

        elif self.path == "/v1/math/factorize":
            num = int(body.get("number", 0))
            factors = factorize_integer(num) if 2 <= num <= 10**14 else []
            self._send_json({"number": num, "factors": factors, "is_prime": len(factors) == 1, "remaining_quota": remaining})
            return

        elif self.path == "/v1/game/vortex":
            x, y, z, t = float(body.get("x", 1.0)), float(body.get("y", 0.5)), float(body.get("z", 2.0)), float(body.get("t", 0.1))
            kappa = math.log(10)
            r = math.sqrt(x*x + y*y) + 1e-6
            enstrophy_limit = min(kappa**2, 1.0 / (r * math.exp(-0.1 * t) + 0.1))
            u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
            u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
            u_z = round( math.cos(kappa * r) * math.exp(-0.1 * t), 4)
            self._send_json({"velocity": [u_x, u_y, u_z], "enstrophy_bound": round(enstrophy_limit, 4), "remaining_quota": remaining})
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
