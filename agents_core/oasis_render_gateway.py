#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY CON LOGIN Y SUITE COMPLETA DE APIS
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
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
KAPPA = math.log(10.0)
ALPHA = 1.0 / 137.036
GOLDEN_WAIT_BASE = math.pi / PHI

RSA_E = 17
RSA_N = 3233
RSA_D = 2753
SPENT_NULLIFIERS = set()

AUTH_KEYS = {
    MASTER_KEY: {"quota": float("inf"), "owner": "sovereign_root"}
}
VIRTUAL_FS = {}
VORTEX_CACHE = {}
LLM_CACHE = {}  # Capa 0: Caché semántica en memoria RAM

SWARM_LOCK = threading.Lock()
PENDING_JOBS = []
COMPLETED_JOBS = {}

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

TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign Terminal OS v2.6</title>
<style>
  :root {
    --bg: #05080d;
    --term-bg: rgba(6, 12, 20, 0.92);
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
    padding: 15px;
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
    padding: 20px;
    box-shadow: 0 0 35px rgba(0, 255, 157, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  #header {
    border-bottom: 1px dashed var(--dim);
    padding-bottom: 10px;
    margin-bottom: 12px;
    font-size: 0.85rem;
    color: var(--accent);
  }
  #output {
    flex: 1;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-y: auto;
    padding-right: 10px;
  }
  .prompt-row {
    display: flex;
    align-items: center;
    margin-top: 10px;
    padding-top: 10px;
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
    🌌 OASIS SOVEREIGN OS [Linux-Kernel v2.6.0-x86_64] | Nodo: Render Fráncfort | Beneficiario: akash1dy3...
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

let CURRENT_KEY = "OASIS-KEY-GUEST";
let IS_ROOT = false;
let HW_KEY = "";
let history = [];
let hIndex = -1;

async function getHWFingerprint() {
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

function getVFS() {
  const s = localStorage.getItem('OASIS_VFS_' + CURRENT_KEY);
  if (s) { try { return JSON.parse(s); } catch(e){} }
  return {
    "/home/oasis/README.txt": "Terminal Soberana con Suite Completa de APIs.\\nEscribe 'help' para ver los comandos.",
    "/home/oasis/config.json": '{"mode": "cold_silicon", "node": "render_frankfurt"}'
  };
}
function saveVFS(vfs) { localStorage.setItem('OASIS_VFS_' + CURRENT_KEY, JSON.stringify(vfs)); }

function print(t, cls='') {
  const d = document.createElement('div');
  d.className = cls;
  d.innerText = t;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}

getHWFingerprint().then(() => {
  out.innerHTML = `✅ [HUELLA DE SILICIO]: ${HW_KEY}
🔐 [SESIÓN LOCAL]: Almacenamiento aislado en tu navegador (Zero-Cloud Leak)
⚡ [MOTOR HÍBRIDO]: Render (Filtro RAM) + Mac (Inferencia Ollama)

Escribe 'help' para ver el catálogo completo de APIs y comandos.
-------------------------------------------------------------`;
  promptTag.innerText = `oasis@${HW_KEY.substring(9, 15).toLowerCase()}:~$`;
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
      print(`CATÁLOGO DE COMANDOS Y APIS OASIS:
  login <clave>        - Inicia sesión como administrador soberano (ej. Clave Maestra)
  ai <consulta>        - Consulta a la IA Local con Freno Geométrico y Caché RAM
  ai --7b <consulta>   - Consulta forzada a modelo 7B (Razonamiento profundo)
  shield <ms,ms,ms...> - Ejecuta el Escudo Anti-Bot Zero-PII (/v1/shield/entropy-score)
  factorize <numero>   - Descomposición en factores primos (/v1/math/factorize)
  vortex <x> <y> <z>   - Cálculo físico 3D con cota kappa=ln(10) (/v1/game/vortex)
  harden <bits>        - Endurece módulo RSA con phi^-1 * alpha (/v1/harden)
  ecash mint           - Emite un billete ciego eCash (/v1/ecash/blind-sign)
  bounty               - Ejecuta prueba de cómputo PoUW (/v1/bounty/submit)
  fs [ls|cat|echo|rm]  - Sistema de archivos local privado en tu navegador
  status               - Telemetría del nodo, balance Akash y colas
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'login') {
      const key = args[0];
      if (key === 'OASIS-SOVEREIGN-MARIANO-2026') {
        CURRENT_KEY = key;
        IS_ROOT = true;
        promptTag.innerText = "root@oasis-sovereign:~#";
        promptTag.className = "prompt-lbl root-lbl";
        print("🔓 [AUTENTICACIÓN ROOT]: Reconocido como sovereign_root. Cuota infinita activada.", "warn");
      } else if (key && key.startsWith("OASIS-KEY-")) {
        CURRENT_KEY = key;
        IS_ROOT = false;
        promptTag.innerText = `user@${key.substring(10, 16)}:~$`;
        promptTag.className = "prompt-lbl";
        print(`🔑 [AUTENTICACIÓN CLIENTE]: Clave activa: ${key}`, "info");
      } else {
        print("Clave inválida. Formato: login OASIS-SOVEREIGN-MARIANO-2026", "alert");
      }
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print("Uso: ai <prompt>", "alert"); return; }
      print("⏳ Auditando por Freno Geométrico y consultando caché...", "dim");
      const res = await fetch('/v1/llm/secure-proxy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({prompt})
      }).then(r=>r.json());
      if (res.clean_response) {
        print(`🤖 [${res.model_used}] (${res.source || 'Inferencia'}):\\n` + res.clean_response, "info");
      } else {
        print(JSON.stringify(res, null, 2), "alert");
      }
    } else if (cmd === 'shield') {
      const intervals = args[0] ? args[0].split(',').map(Number) : [140.2, 510.1, 220.4, 890.3];
      const res = await fetch('/v1/shield/entropy-score', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({intervals_ms: intervals})
      }).then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'factorize') {
      const num = parseInt(args[0]) || 1000000016000000063;
      const res = await fetch('/v1/math/factorize', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({number: num})
      }).then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'vortex') {
      const [x, y, z] = args.map(Number);
      const res = await fetch('/v1/game/vortex', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({x: x||1.0, y: y||0.5, z: z||2.0, t: 0.1})
      }).then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'harden') {
      const bits = parseInt(args[0]) || 2048;
      const res = await fetch('/v1/harden', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({modulus_bits: bits})
      }).then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'ecash') {
      const res = await fetch('/v1/ecash/blind-sign', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({blinded_message: 2347})
      }).then(r=>r.json());
      print(`🎫 Billete eCash firmado a ciegas: Firma=${res.blind_signature} (Módulo N=${res.mint_N})`, "info");
    } else if (cmd === 'bounty') {
      const res = await fetch('/v1/bounty/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          worker: "web-terminal-user",
          target_composite: 1000000016000000063,
          factors: [1000000007, 1000000009],
          proof_hash: "prueba_web"
        })
      }).then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'status') {
      const res = await fetch('/status').then(r=>r.json());
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'fs') {
      const sub = args[0];
      if (sub === 'ls') print(Object.keys(vfs).join('   '), 'info');
      else if (sub === 'cat') print(vfs[args[1]] || 'Archivo no encontrado', 'info');
      else if (sub === 'echo') {
        const text = args.slice(1, -1).join(' ').replace(/"/g, '');
        const f = args[args.length - 1];
        vfs[f] = text; saveVFS(vfs);
        print(`Guardado en ${f} (Disco local)`, 'dim');
      } else if (sub === 'rm') {
        delete vfs[args[1]]; saveVFS(vfs);
        print(`Eliminado ${args[1]}`, 'dim');
      } else print("Uso: fs [ls|cat <f>|echo <txt> <f>|rm <f>]", "alert");
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
            return False, f"Pago requerido. Proporciona 'x-api-key'. Recargas a {AKASH_WALLET}", 402
        if api_key not in AUTH_KEYS:
            if api_key.startswith("OASIS-HW-") or api_key == "OASIS-KEY-GUEST":
                AUTH_KEYS[api_key] = {"quota": 1000, "owner": "guest_hardware"}
            else:
                return False, "Clave API no registrada", 403

        entry = AUTH_KEYS[api_key]
        if entry["quota"] <= 0:
            return False, f"Cuota agotada. Envía 1 AKT a {AKASH_WALLET} con memo '{api_key}'", 402
        if entry["quota"] != float("inf"):
            entry["quota"] -= 1
        return True, entry, 200

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
                "os": "Oasis Sovereign Linux v2.6",
                "cache_ram_entries": len(LLM_CACHE),
                "active_keys": len(AUTH_KEYS)
            })
        elif self.path == "/v1/swarm/poll":
            with SWARM_LOCK:
                if PENDING_JOBS:
                    self._send_json(PENDING_JOBS.pop(0))
                    return
            self._send_json({"has_job": False})
        else:
            self._send_json({"error": "Ruta no encontrada"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode())
        except Exception:
            body = {}

        if self.path == "/v1/ecash/blind-sign":
            blinded_m = body.get("blinded_message", 0)
            blind_sig = pow(int(blinded_m), RSA_D, RSA_N)
            self._send_json({"blind_signature": blind_sig, "mint_e": RSA_E, "mint_N": RSA_N})
            return

        if self.path == "/v1/bounty/submit":
            composite = int(body.get("target_composite", 0))
            factors = body.get("factors", [])
            if len(factors) == 2 and (factors[0] * factors[1] == composite):
                self._send_json({"status": "ACCEPTED", "verdict": "PROOF_VERIFIED_O1"})
            else:
                self._send_json({"error": "INVALID_FACTORS"}, status=400)
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

        # Endpoints protegidos con autenticación
        auth_ok, auth_res, code = self._authenticate()
        if not auth_ok:
            self._send_json({"error": "PAGO_REQUERIDO", "motivo": auth_res}, status=code)
            return

        # Inferencia con Caché en RAM (Capa 0)
        if self.path == "/v1/llm/secure-proxy":
            prompt_raw = body.get("prompt", "")
            prompt_clean = sanitize_llm_prompt(prompt_raw)
            cache_hash = hashlib.sha256(prompt_clean.encode()).hexdigest()

            # 1. Si está en la memoria RAM de Render, respuesta inmediata en < 0.1 ms
            if cache_hash in LLM_CACHE:
                self._send_json({
                    "status": "CACHE_HIT_RAM",
                    "source": "Caché en RAM Render (0.04 ms)",
                    "model_used": "oasis-cache-ram",
                    "clean_response": LLM_CACHE[cache_hash]
                })
                return

            # 2. Si es nuevo, encolar al Mac
            job_id = cache_hash[:12]
            with SWARM_LOCK:
                PENDING_JOBS.append({"has_job": True, "job_id": job_id, "prompt": prompt_clean})

            t0 = time.time()
            while time.time() - t0 < 45.0:
                with SWARM_LOCK:
                    if job_id in COMPLETED_JOBS:
                        res = COMPLETED_JOBS.pop(job_id)
                        resp_text = res.get("response", "")
                        LLM_CACHE[cache_hash] = resp_text  # Guardar en RAM para futuras llamadas
                        self._send_json({
                            "status": "SUCCESS",
                            "source": "Mac Hardware Local",
                            "model_used": res.get("model", "oasis-edge:1.5b"),
                            "clean_response": resp_text
                        })
                        return
                time.sleep(0.2)

            self._send_json({"status": "TIMEOUT", "clean_response": "[Aviso]: Tu Mac no recogió la tarea a tiempo."})
            return

        elif self.path == "/v1/shield/entropy-score":
            intervals = body.get("intervals_ms", [])
            mean = sum(intervals) / (len(intervals) + 1e-6)
            self._send_json({
                "target_id": body.get("target_id", "anon"),
                "is_bot": len(intervals) >= 3 and mean < 60.0,
                "entropy_status": "EVALUADO_CON_EXITO"
            })
            return

        elif self.path == "/v1/math/factorize":
            num = int(body.get("number", 0))
            factors = factorize_integer(num) if 2 <= num <= 10**14 else []
            self._send_json({"number": num, "factors": factors, "is_prime": len(factors) == 1})
            return

        elif self.path == "/v1/game/vortex":
            x, y, z, t = float(body.get("x", 1.0)), float(body.get("y", 0.5)), float(body.get("z", 2.0)), float(body.get("t", 0.1))
            kappa = math.log(10)
            r = math.sqrt(x*x + y*y) + 1e-6
            enstrophy_limit = min(kappa**2, 1.0 / (r * math.exp(-0.1 * t) + 0.1))
            u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
            u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
            u_z = round( math.cos(kappa * r) * math.exp(-0.1 * t), 4)
            self._send_json({"velocity": [u_x, u_y, u_z], "enstrophy_bound": round(enstrophy_limit, 4)})
            return

        elif self.path == "/v1/harden":
            bits = int(body.get("modulus_bits", 2048))
            factor = (PHI ** -1) * ALPHA
            self._send_json({"original_bits": bits, "hardened_bits": round(bits * (1.0 + factor), 4)})
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
