#!/usr/bin/env python3
import os
import json
import math
import struct
import hashlib
import threading
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
RPC_NODE = "https://rpc.akashnet.net:443"
SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"
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
VIRTUAL_FS = {}  # Memoria virtual de bloques fragmentados {filename: [chunks]}

VORTEX_CACHE = {}
MAX_CACHE_ENTRIES = 25000

# HTML/JS de la Terminal Soberana
TERMINAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oasis Sovereign Terminal OS</title>
<style>
  :root { --bg: #0a0e14; --fg: #00ff88; --dim: #007744; --accent: #00e5ff; }
  body { background: var(--bg); color: var(--fg); font-family: 'Courier New', monospace; margin: 0; padding: 20px; box-sizing: border-box; }
  #terminal { max-width: 900px; margin: 0 auto; background: rgba(0,20,10,0.4); border: 1px solid var(--dim); border-radius: 8px; padding: 20px; box-shadow: 0 0 20px rgba(0,255,136,0.15); }
  #output { white-space: pre-wrap; word-break: break-all; margin-bottom: 15px; max-height: 70vh; overflow-y: auto; }
  .prompt-line { display: flex; align-items: center; }
  .prompt { color: var(--accent); font-weight: bold; margin-right: 10px; }
  input { flex: 1; background: transparent; border: none; outline: none; color: var(--fg); font-family: inherit; font-size: 1rem; }
  .dim { color: var(--dim); }
  .info { color: var(--accent); }
</style>
</head>
<body>
<div id="terminal">
  <div id="output">
  🌌 OASIS SOVEREIGN OS [Terminal v2.4 - Silicio Frío]
  Conectado a nodo: Render (Fráncfort) | Red: Cosmos IBC / Akash Network
  Escribe 'help' para ver los comandos disponibles.
  -------------------------------------------------------------
  </div>
  <div class="prompt-line">
    <span class="prompt">oasis@node:~$</span>
    <input type="text" id="cmd" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
  </div>
</div>

<script>
const out = document.getElementById('output');
const input = document.getElementById('cmd');

function print(text, cls='') {
  const div = document.createElement('div');
  div.className = cls;
  div.innerText = text;
  out.appendChild(div);
  out.scrollTop = out.scrollHeight;
}

input.addEventListener('keydown', async (e) => {
  if (e.key === 'Enter') {
    const raw = input.value.trim();
    if (!raw) return;
    print('oasis@node:~$ ' + raw, 'dim');
    input.value = '';
    const parts = raw.split(' ');
    const command = parts[0].toLowerCase();
    const args = parts.slice(1);

    if (command === 'help') {
      print(`COMANDOS DISPONIBLES:
  status               - Estado del nodo, balance y telemetría
  ai <prompt>          - Consulta segura con Freno Geométrico
  vortex <x> <y> <z>   - Simulación de fluidos determinista (16 bytes)
  fs put <name> <txt>  - Fragmenta y almacena un archivo en bloques
  fs get <name>        - Desfragmenta y lee el archivo
  fs list              - Lista archivos en el disco virtual
  ecash                - Muestra saldo y genera ticket de pago ciego
  clear                - Limpia la pantalla`);
    } else if (command === 'clear') {
      out.innerHTML = '';
    } else if (command === 'status') {
      const res = await fetch('/status').then(r=>r.json());
      print(JSON.stringify(res, null, 2), 'info');
    } else if (command === 'ai') {
      const prompt = args.join(' ');
      print('⏳ Auditando entropía y evaluando prompt...', 'dim');
      const res = await fetch('/v1/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
        body: JSON.stringify({prompt})
      }).then(r=>r.json());
      print(`Evaluación: ${res.verdict} | Entropía: ${res.shannon_entropy} | Retardo: ${res.recommended_wait_sec}s`, 'info');
    } else if (command === 'vortex') {
      const [x, y, z] = args.map(Number);
      const res = await fetch('/v1/game/vortex', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': 'OASIS-SOVEREIGN-MARIANO-2026'},
        body: JSON.stringify({x: x||1.0, y: y||0.5, z: z||2.0, t: 0.1})
      }).then(r=>r.json());
      print(`Velocidad: [${res.velocity}] | Enstrofía: ${res.enstrophy_bound}`, 'info');
    } else if (command === 'fs') {
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
        if (res.content) {
          print(`Contenido reensamblado: "${res.content}"`, 'info');
        } else {
          print('Archivo no encontrado', 'dim');
        }
      } else if (sub === 'list') {
        const res = await fetch('/v1/fs/list').then(r=>r.json());
        print('Archivos: ' + res.files.join(', '), 'info');
      }
    } else {
      print(`Comando desconocido: '${command}'. Escribe 'help'.`, 'dim');
    }
  }
});
</script>
</body>
</html>
"""

def compute_game_vortex(x, y, z, t, helicity=1.0):
    cache_key = hashlib.sha256(f"{x:.4f}:{y:.4f}:{z:.4f}:{t:.4f}:{helicity:.4f}".encode()).hexdigest()
    if cache_key in VORTEX_CACHE:
        return VORTEX_CACHE[cache_key], True, cache_key

    kappa = math.log(10)
    r = math.sqrt(x*x + y*y) + 1e-6
    decay = math.exp(-0.1 * t)
    enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))

    u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_z = round( math.cos(kappa * r) * decay, 4)
    res = ([u_x, u_y, u_z], round(enstrophy_limit, 4))
    if len(VORTEX_CACHE) < MAX_CACHE_ENTRIES:
        VORTEX_CACHE[cache_key] = res
    return res, False, cache_key

def shannon_entropy(text: str) -> float:
    if not text: return 0.0
    freq = {}
    for c in text: freq[c] = freq.get(c, 0) + 1
    ent = 0.0
    n = len(text)
    for count in freq.values():
        p = count / n
        ent -= p * math.log2(p)
    return round(ent, 4)

class OasisCloudHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key, x-oasis-ecash")
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
            self.wfile.write(TERMINAL_HTML.encode("utf-8"))
        elif self.path in ("/telemetry", "/healthz"):
            self._send_json({
                "status": "ONLINE",
                "system": "Oasis Sovereign Monolith & Web Terminal OS",
                "akash_beneficiary": AKASH_WALLET,
                "virtual_files_count": len(VIRTUAL_FS)
            })
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "wallet": AKASH_WALLET,
                "endpoints": ["/v1/verify", "/v1/game/vortex", "/v1/fs/put", "/v1/fs/get"]
            })
        elif self.path.startswith("/v1/fs/get"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            fname = query.get("filename", [""])[0]
            if fname in VIRTUAL_FS:
                # Desfragmentación: Reensambla los bloques ordenados
                chunks = VIRTUAL_FS[fname]
                full_content = "".join(chunks)
                self._send_json({"filename": fname, "content": full_content, "reassembled_chunks": len(chunks)})
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

        # Fragmentación y almacenamiento virtual
        if self.path == "/v1/fs/put":
            filename = body.get("filename", "unnamed.dat")
            content = body.get("content", "")
            chunk_size = 32  # Micro-bloques para demostración
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            VIRTUAL_FS[filename] = chunks
            root_hash = hashlib.sha256(content.encode()).hexdigest()
            self._send_json({"filename": filename, "chunks_created": len(chunks), "root_merkle": root_hash})
            return

        elif self.path == "/v1/verify":
            prompt = body.get("prompt", "")
            ent = shannon_entropy(prompt)
            ratio = (len(prompt) + 1) / (ent + 1)
            deviation = abs(ratio - KAPPA)
            is_suspicious = deviation > 0.8 or ent < 1.5
            wait = GOLDEN_WAIT_BASE * (1.0 + deviation) if is_suspicious else 0.0
            self._send_json({
                "prompt_length": len(prompt),
                "shannon_entropy": ent,
                "is_safe": not is_suspicious,
                "recommended_wait_sec": round(wait, 4),
                "verdict": "APPLY_BRAKE" if is_suspicious else "FORWARD_TO_LLM"
            })
            return

        elif self.path == "/v1/game/vortex":
            x, y, z, t = float(body.get("x", 1.0)), float(body.get("y", 0.5)), float(body.get("z", 2.0)), float(body.get("t", 0.1))
            (vel, enstrophy), is_cached, _ = compute_game_vortex(x, y, z, t)
            self._send_json({
                "velocity": vel,
                "enstrophy_bound": enstrophy,
                "cache_hit": is_cached
            })
            return

        self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
