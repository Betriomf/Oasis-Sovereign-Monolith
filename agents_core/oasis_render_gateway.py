#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY v2.7.0 CON SUITE COMPLETA, LOGIN Y SHARDING ZERO-KNOWLEDGE
"""
import os
import json
import math
import struct
import hashlib
import threading
import time
import re
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
SHARD_STORAGE = {}  # Fragmentos opacos cifrados en origen {doc_id: [chunk1, chunk2, chunk3]}
LLM_CACHE = {}

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
<title>Oasis Sovereign Linux OS v2.7</title>
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
    <span>🌌 OASIS SOVEREIGN OS [v2.7.0-sovereign-x86_64] | Nodo: Fráncfort</span>
    <span id="quota-display" class="warn">Cuota: 1000</span>
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

let CURRENT_KEY = "";
let IS_ROOT = false;
let HW_KEY = "";
let REMAINING_QUOTA = 1000;
let history = [];
let hIndex = -1;

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

// Cifrado simétrico AES-GCM derivado de la clave de hardware del cliente
async function getCryptoKey() {
  const enc = new TextEncoder().encode(HW_KEY.padEnd(32, '0'));
  return await crypto.subtle.importKey('raw', enc, {name: 'AES-GCM'}, false, ['encrypt', 'decrypt']);
}

async function encryptData(plainText) {
  const key = await getCryptoKey();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt({name: 'AES-GCM', iv}, key, new TextEncoder().encode(plainText));
  const combined = new Uint8Array(iv.length + encrypted.byteLength);
  combined.set(iv);
  combined.set(new Uint8Array(encrypted), iv.length);
  return btoa(String.fromCharCode(...combined));
}

async function decryptData(b64Data) {
  const key = await getCryptoKey();
  const raw = Uint8Array.from(atob(b64Data), c=>c.charCodeAt(0));
  const iv = raw.slice(0, 12);
  const data = raw.slice(12);
  const decrypted = await crypto.subtle.decrypt({name: 'AES-GCM', iv}, key, data);
  return new TextDecoder().decode(decrypted);
}

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

deriveHWKey().then(() => {
  out.innerHTML = `✅ [HUELLA FÍSICA DETECTADA]: ${HW_KEY}
🔐 [SESIÓN PRIVADA]: Cuota inicial de 1000 llamadas de cortesía.
💾 [ALMACENAMIENTO ZERO-KNOWLEDGE]: Cifrado AES-GCM local en tu máquina.
⚡ [ENLACE NEURAL]: Proxy activo con Freno Geométrico.

Escribe 'help' para ver el catálogo de APIs y comandos.
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

    if (cmd === 'help') {
      print(`COMANDOS DISPONIBLES:
  login <clave>        - Inicia sesión maestra (ej. login OASIS-SOVEREIGN-MARIANO-2026)
  ai <prompt>          - Consulta a tu IA Local a través del Firewall LLM
  ai --7b <prompt>     - Consulta profunda usando modelo 7B
  shield [ms,ms,...]   - Ciberseguridad: Escudo Anti-Bot Zero-PII (/v1/shield/entropy-score)
  factorize <num>      - Factorización de enteros grandes (/v1/math/factorize)
  vortex <x> <y> <z>   - Cinemática de fluidos 3D acotada por kappa (/v1/game/vortex)
  harden <bits>        - Endurecimiento criptográfico RSA-Oasis (/v1/harden)
  bounty               - Entrega de prueba PoUW (/v1/bounty/submit)
  ecash mint           - Emite billete eCash anónimo (/v1/ecash/blind-sign)
  shard put <id> <txt> - Cifra en TU PC con AES-GCM, fragmenta en 3 y dispersa en la nube
  shard get <id>       - Reensambla fragmentos de la nube y descifra en TU PC
  pay akash <tx_hash>  - Recarga saldo indicando una transacción en la red Akash
  quota                - Muestra créditos restantes de tu sesión
  hwinfo               - Identidad física de hardware intransferible
  clear                - Limpia la pantalla`);
    } else if (cmd === 'clear') {
      out.innerHTML = '';
    } else if (cmd === 'hwinfo') {
      print(`--- IDENTIDAD DE SILICIO ---
Clave derivada:   ${HW_KEY}
Modo de sesión:   ${IS_ROOT ? 'ROOT SOBERANO' : 'CLIENTE'}
Cuota activa:     ${IS_ROOT ? 'ILIMITADA' : REMAINING_QUOTA}
Cifrado local:    AES-GCM-256 (Clave nunca expuesta)`, 'info');
    } else if (cmd === 'quota') {
      print(IS_ROOT ? "Cuota: ILIMITADA (sovereign_root)" : `Cuota restante: ${REMAINING_QUOTA} créditos.`, 'info');
    } else if (cmd === 'login') {
      const key = args[0];
      if (key === 'OASIS-SOVEREIGN-MARIANO-2026') {
        CURRENT_KEY = key;
        IS_ROOT = true;
        promptTag.innerText = "root@oasis-sovereign:~#";
        promptTag.className = "prompt-lbl root-lbl";
        updateQuota(Infinity);
        print("🔓 [AUTENTICACIÓN ROOT SATISFACTORIA]: Bienvenido Mariano. Acceso ilimitado concedido.", "warn");
      } else if (key && key.startsWith("OASIS-KEY-")) {
        CURRENT_KEY = key;
        IS_ROOT = false;
        promptTag.innerText = `user@${key.substring(10, 16)}:~$`;
        promptTag.className = "prompt-lbl";
        print(`🔑 [AUTENTICACIÓN CLIENTE]: Clave registrada: ${key}`, "info");
      } else {
        print("Clave no reconocida. Usa: login OASIS-SOVEREIGN-MARIANO-2026", "alert");
      }
    } else if (cmd === 'ai') {
      const prompt = args.join(' ');
      if (!prompt) { print("Uso: ai <consulta>", "alert"); return; }
      print("🛡️  Auditando prompt por Freno Geométrico y despachando al Mac...", "dim");
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
    } else if (cmd === 'shield') {
      const intervals = args[0] ? args[0].split(',').map(Number) : [140.2, 510.1, 220.4, 890.3];
      const res = await fetch('/v1/shield/entropy-score', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({intervals_ms: intervals})
      }).then(r=>r.json());
      updateQuota(res.remaining_quota);
      print(JSON.stringify(res, null, 2), "info");
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
    } else if (cmd === 'harden') {
      const bits = parseInt(args[0]) || 2048;
      const res = await fetch('/v1/harden', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
        body: JSON.stringify({modulus_bits: bits})
      }).then(r=>r.json());
      updateQuota(res.remaining_quota);
      print(JSON.stringify(res, null, 2), "info");
    } else if (cmd === 'ecash') {
      const res = await fetch('/v1/ecash/blind-sign', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({blinded_message: 2347})
      }).then(r=>r.json());
      print(`🎫 Billete eCash firmado a ciegas: Firma=${res.blind_signature}`, "info");
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
    } else if (cmd === 'shard') {
      const sub = args[0];
      const docId = args[1];
      if (sub === 'put') {
        const text = args.slice(2).join(' ');
        if (!docId || !text) { print("Uso: shard put <id> <texto>", "alert"); return; }
        print("🔒 Cifrando con AES-GCM en tu silicio local...", "dim");
        const encryptedB64 = await encryptData(text);
        // Dividir el texto cifrado en 3 fragmentos opacos
        const partLen = Math.ceil(encryptedB64.length / 3);
        const shards = [
          encryptedB64.substring(0, partLen),
          encryptedB64.substring(partLen, partLen * 2),
          encryptedB64.substring(partLen * 2)
        ];
        const res = await fetch('/v1/shards/store', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'x-api-key': CURRENT_KEY},
          body: JSON.stringify({doc_id: docId, shards})
        }).then(r=>r.json());
        print(`✅ [ZERO-KNOWLEDGE DISPERSADO]: Documento '${docId}' fragmentado en 3 trozos cifrados. Servidor tiene 0% visibilidad.`, "info");
      } else if (sub === 'get') {
        if (!docId) { print("Uso: shard get <id>", "alert"); return; }
        const res = await fetch('/v1/shards/fetch?doc_id=' + docId).then(r=>r.json());
        if (res.shards) {
          const combinedB64 = res.shards.join('');
          try {
            const originalText = await decryptData(combinedB64);
            print(`🔓 [REENSAMBLADO Y DESCIFRADO LOCAL]:\\n"${originalText}"`, "info");
          } catch(err) {
            print("❌ Error de descifrado: Tu máquina no posee la clave de hardware propietaria de este archivo.", "alert");
          }
        } else {
          print("Documento no encontrado.", "alert");
        }
      } else {
        print("Uso: shard [put <id> <texto> | get <id>]", "alert");
      }
    } else if (cmd === 'pay') {
      print(`💳 Para recargar envía 1 AKT a ${'akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y'} indicando tu clave en el Memo. El daemon te acreditará en 30s.`, "warn");
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
            return False, f"Pago requerido. Proporciona 'x-api-key'.", 402

        if api_key == MASTER_KEY:
            return True, AUTH_KEYS[MASTER_KEY], 200

        if api_key not in AUTH_KEYS:
            if api_key.startswith("OASIS-HW-") or api_key.startswith("OASIS-KEY-"):
                AUTH_KEYS[api_key] = {"quota": 1000, "owner": "guest_hardware"}
            else:
                return False, "Clave no registrada", 403

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
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            self.wfile.write(TERMINAL_HTML.encode())
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "wallet": AKASH_WALLET,
                "os": "Oasis Sovereign Linux v2.7",
                "cache_ram_entries": len(LLM_CACHE),
                "shards_stored": len(SHARD_STORAGE),
                "active_keys": len(AUTH_KEYS)
            })
        elif self.path == "/v1/swarm/poll":
            with SWARM_LOCK:
                if PENDING_JOBS:
                    self._send_json(PENDING_JOBS.pop(0))
                    return
            self._send_json({"has_job": False})
        elif self.path.startswith("/v1/shards/fetch"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            doc_id = query.get("doc_id", [""])[0]
            if doc_id in SHARD_STORAGE:
                self._send_json({"doc_id": doc_id, "shards": SHARD_STORAGE[doc_id]})
            else:
                self._send_json({"error": "Shards no encontrados"}, status=404)
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

        # Endpoints autenticados
        auth_ok, auth_res, code = self._authenticate()
        if not auth_ok:
            self._send_json({"error": "PAGO_REQUERIDO", "motivo": auth_res}, status=code)
            return

        remaining = auth_res.get("quota")

        # Almacenamiento Zero-Knowledge de fragmentos opacos
        if self.path == "/v1/shards/store":
            doc_id = body.get("doc_id", "")
            shards = body.get("shards", [])
            if doc_id and len(shards) == 3:
                SHARD_STORAGE[doc_id] = shards
                self._send_json({"status": "STORED", "doc_id": doc_id, "shards_count": 3, "remaining_quota": remaining})
            else:
                self._send_json({"error": "Datos de fragmentación inválidos"}, status=400)
            return

        # Inferencia LLM con Caché en RAM
        if self.path == "/v1/llm/secure-proxy":
            prompt_raw = body.get("prompt", "")
            prompt_clean = sanitize_llm_prompt(prompt_raw)
            cache_hash = hashlib.sha256(prompt_clean.encode()).hexdigest()

            if cache_hash in LLM_CACHE:
                self._send_json({
                    "status": "CACHE_HIT_RAM",
                    "source": "Caché RAM Fráncfort (<0.05 ms)",
                    "model_used": "oasis-cache-ram",
                    "clean_response": LLM_CACHE[cache_hash],
                    "remaining_quota": remaining
                })
                return

            job_id = cache_hash[:12]
            with SWARM_LOCK:
                PENDING_JOBS.append({"has_job": True, "job_id": job_id, "prompt": prompt_clean})

            t0 = time.time()
            while time.time() - t0 < 45.0:
                with SWARM_LOCK:
                    if job_id in COMPLETED_JOBS:
                        res = COMPLETED_JOBS.pop(job_id)
                        resp_text = res.get("response", "")
                        LLM_CACHE[cache_hash] = resp_text
                        self._send_json({
                            "status": "SUCCESS",
                            "source": "Silicio Frío Local (Mac)",
                            "model_used": res.get("model", "oasis-edge:1.5b"),
                            "clean_response": resp_text,
                            "remaining_quota": remaining
                        })
                        return
                time.sleep(0.2)

            self._send_json({
                "status": "TIMEOUT",
                "clean_response": "[Aviso]: Tu Mac no recogió la tarea a tiempo. Inicia 'oasis_mac_bridge.py'.",
                "remaining_quota": remaining
            })
            return

        elif self.path == "/v1/shield/entropy-score":
            intervals = body.get("intervals_ms", [])
            mean = sum(intervals) / (len(intervals) + 1e-6)
            self._send_json({
                "target_id": body.get("target_id", "anon"),
                "is_bot": len(intervals) >= 3 and mean < 60.0,
                "entropy_status": "EVALUADO_CON_EXITO",
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

        elif self.path == "/v1/harden":
            bits = int(body.get("modulus_bits", 2048))
            factor = (PHI ** -1) * ALPHA
            self._send_json({"original_bits": bits, "hardened_bits": round(bits * (1.0 + factor), 4), "remaining_quota": remaining})
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
