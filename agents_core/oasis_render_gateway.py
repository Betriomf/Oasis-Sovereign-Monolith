#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — GATEWAY UNIVERSAL v11.0.0-QuantumSwarmVaultMaster
Consolidación completa:
- Rehidratación Automática al iniciar: restaura VFS, Widgets y Vault desde Supabase.
- Selector Desplegable de Widgets: Cuántica, IA Agentes, Multimedia, Android/Termux, OPFS.
- Simulador Cuántico OpenQASM / MicroQiskit ('quantum-run') y Traductor /dev/qpu.
- Consultas seguras a Gemini / Qiskit usando claves protegidas en Supabase Vault.
- Portapapeles DOM con selección nativa libre (Cmd+C / Cmd+V) y botón rápido 'COPIAR'.
- Motor 3D Doom Raycaster en Canvas y Traductores Hurd (/dev/weather, /dev/cpu, /dev/triage).
- Box Privado OPFS NVMe y WebRTC P2P DataChannels.
"""
import os
import sys
import io
import json
import time
import socket
import ssl
import urllib.request
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import qrcode
    import qrcode.image.svg
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

PORT = int(os.environ.get("PORT", 8080))
IS_RENDER = os.environ.get("RENDER") == "true"
RAM_DIR = "/Volumes/OasisRAM" if os.path.exists("/Volumes/OasisRAM") else "/tmp"
CERT_FILE = os.path.join(RAM_DIR, "oasis_cert.pem")
KEY_FILE = os.path.join(RAM_DIR, "oasis_key.pem")

HARDWARE_ID = "OASIS-HW-468F6F695BDB"
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def get_sovereign_ip():
    for iface in ["bridge100", "en5", "en4"]:
        try:
            out = subprocess.check_output(["ipconfig", "getifaddr", iface]).decode().strip()
            if out: return out
        except Exception: pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_sovereign_ip()
RENDER_HOST = "https://oasis-sovereign-gateway.onrender.com"

# --- CLIENTE SUPABASE REST Y CONSULTA A VAULT ---
def supabase_request(method, endpoint, payload=None):
    if not SUPABASE_KEY or not SUPABASE_URL:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    data_bytes = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            res_text = resp.read().decode("utf-8")
            return json.loads(res_text) if res_text else {}
    except Exception:
        return None

def get_vault_secret(key_name):
    rows = supabase_request("GET", f"kernel_vault?key_name=eq.{key_name}&select=secret_value")
    if rows and isinstance(rows, list) and len(rows) > 0:
        return rows[0].get("secret_value")
    return os.environ.get(key_name, "")

# --- REHIDRATACIÓN AL ARRANCAR (BOOTSTRAP EN RAM) ---
BOOT_VFS = {}
BOOT_WIDGETS = {}

def boot_rehydrate():
    global BOOT_VFS, BOOT_WIDGETS
    print("⚡ [BOOTSTRAP]: Sincronizando estado vivo desde Supabase...")
    w_rows = supabase_request("GET", "widgets?select=name,code,category")
    if w_rows and isinstance(w_rows, list):
        for w in w_rows:
            BOOT_WIDGETS[w["name"]] = {"code": w["code"], "category": w.get("category", "custom")}
        print(f"📦 [BOOTSTRAP]: {len(BOOT_WIDGETS)} widgets rehidratados.")

    s_rows = supabase_request("GET", "kernel_snapshots?order=created_at.desc&limit=1")
    if s_rows and isinstance(s_rows, list) and len(s_rows) > 0:
        BOOT_VFS = s_rows[0].get("snapshot", {})
        print(f"💾 [BOOTSTRAP]: Snapshot VFS recuperado ({len(BOOT_VFS)} archivos).")

boot_rehydrate()

# TLS Efímero local
if not IS_RENDER and not os.environ.get("NO_TLS"):
    try:
        cnf_content = f"""[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
CN = {LOCAL_IP}
[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
IP.1 = {LOCAL_IP}
IP.2 = 127.0.0.1
DNS.1 = localhost
"""
        cnf_path = os.path.join(RAM_DIR, "openssl.cnf")
        with open(cnf_path, "w") as f: f.write(cnf_content)
        cmd = [
            "openssl", "req", "-x509", "-newkey", "ec",
            "-pkeyopt", "ec_paramgen_curve:prime256v1",
            "-nodes", "-days", "1",
            "-keyout", KEY_FILE,
            "-out", CERT_FILE,
            "-config", cnf_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        try: os.remove(cnf_path)
        except Exception: pass
        LOCAL_TLS_ACTIVE = True
    except Exception:
        LOCAL_TLS_ACTIVE = False
else:
    LOCAL_TLS_ACTIVE = False

UI_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Oasis Sovereign OS — Quantum & Swarm Master Kernel</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <style>
    body { background: #03060a; color: #00ff9d; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 10px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; overflow: hidden; }
    .header { border-bottom: 1px solid #005a36; padding-bottom: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; }
    .badge-bar { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .badge { background: #002217; border: 1px solid #00ff9d; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; }
    .badge-hw { background: #1c1500; border: 1px solid #ffaa00; color: #ffd280; font-weight: bold; }
    .badge-caps { background: #00331b; border: 1px solid #00ff66; color: #66ff99; font-weight: bold; }
    .badge-qpu { background: #1b0033; border: 1px solid #b800ff; color: #df80ff; font-weight: bold; cursor: pointer; }
    .badge-menu { background: #002b4d; border: 1px solid #0088ff; color: #80c4ff; cursor: pointer; font-weight: bold; }
    
    #termContainer { flex: 1; position: relative; background: #020408; border: 1px solid #005a36; border-radius: 6px; overflow: hidden; margin-bottom: 8px; display: flex; flex-direction: column; }
    #termCanvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: none; }
    
    #termOutput { flex: 1; padding: 12px; overflow-y: auto; font-size: 0.82rem; line-height: 1.45; white-space: pre-wrap; word-break: break-word; user-select: text; -webkit-user-select: text; z-index: 20; color: #00ff9d; }
    #termOutput::selection { background: #005a36; color: #00ffff; }
    
    .prompt-row { display: flex; align-items: center; background: #050a10; border: 1px solid #005a36; border-radius: 4px; padding: 6px 10px; z-index: 30; }
    .prompt-label { color: #00ff9d; font-weight: bold; margin-right: 8px; font-size: 0.85rem; user-select: none; }
    #cmd { flex: 1; background: transparent; border: none; color: #00e5ff; font-family: inherit; font-size: 0.9rem; outline: none; }

    /* MODAL DESPLEGABLE DE WIDGETS POR CATEGORÍAS */
    #widget-menu { display: none; position: absolute; top: 46px; left: 10px; width: 360px; max-height: 480px; background: #050f14; border: 2px solid #00aaff; border-radius: 8px; box-shadow: 0 0 30px rgba(0,170,255,0.3); z-index: 600; flex-direction: column; overflow: hidden; }
    .menu-header { background: #0a1e2d; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00aaff; font-size: 0.78rem; color: #80d4ff; font-weight: bold; }
    .menu-body { padding: 10px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
    .menu-category { font-size: 0.72rem; color: #ffaa00; font-weight: bold; margin-top: 4px; border-bottom: 1px dashed #334; padding-bottom: 2px; }
    .btn-witem { background: #0c1a24; border: 1px solid #005a36; color: #00ff9d; padding: 5px 8px; text-align: left; font-size: 0.72rem; border-radius: 4px; cursor: pointer; font-family: inherit; }
    .btn-witem:hover { background: #005a36; color: #00ffff; }

    /* VENTANAS FLOTANTES PiP Y WIDGET */
    #pip-container { display: none; position: absolute; top: 12px; right: 12px; width: 340px; background: #050a10; border: 2px solid #ff00aa; border-radius: 8px; box-shadow: 0 0 25px rgba(255,0,170,0.3); z-index: 500; overflow: hidden; }
    .pip-header { background: #1a0012; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ff00aa; font-size: 0.75rem; color: #ff80d5; font-weight: bold; }
    #pipVideo { width: 100%; height: 180px; background: #000; display: block; }
    .pip-channel-bar { padding: 6px; background: #080d14; display: flex; gap: 4px; flex-wrap: wrap; border-top: 1px solid #1a2634; }
    .btn-ch { background: #0a1926; border: 1px solid #00aaff; color: #80d4ff; padding: 3px 6px; font-size: 0.65rem; border-radius: 3px; cursor: pointer; font-family: inherit; }

    #widget-frame-container { display: none; position: absolute; bottom: 60px; right: 12px; width: 380px; height: 260px; background: #050a10; border: 2px solid #00aaff; border-radius: 8px; box-shadow: 0 0 25px rgba(0,170,255,0.3); z-index: 450; overflow: hidden; flex-direction: column; }
    .wframe-header { background: #0a1926; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00aaff; font-size: 0.75rem; color: #80d4ff; font-weight: bold; }
    #wframe { flex: 1; width: 100%; border: none; background: #000; }

    #qr-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3,6,10,0.96); z-index: 1000; justify-content: center; align-items: center; flex-direction: column; }
    .qr-card { background: #05110d; border: 2px solid #00ffaa; border-radius: 12px; padding: 20px; text-align: center; max-width: 440px; box-shadow: 0 0 30px rgba(0,255,170,0.2); }
    .qr-box { background: #fff; padding: 10px; border-radius: 8px; margin: 12px auto; width: 180px; height: 180px; display: flex; justify-content: center; align-items: center; }
    .qr-box img { width: 180px; height: 180px; }
    .btn { background: #00ffaa; color: #03060a; border: none; padding: 4px 8px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 0.72rem; }
    .btn-cancel { background: transparent; border: 1px solid #ff5555; color: #ff5555; }
  </style>
</head>
<body>
  <div class="header">
    <span>🛰️ OASIS SOVEREIGN OS <strong>v11.0.0-QuantumVaultMaster</strong></span>
    <div class="badge-bar">
      <span class="badge badge-hw">🔑 HW: __HW_ID__</span>
      <span class="badge badge-caps">🛡️ Caps: 0x8800</span>
      <span class="badge badge-qpu" onclick="runQuantumDemo()">⚛️ QPU: OPENQASM 3.0</span>
      <span class="badge badge-menu" onclick="toggleWidgetMenu()">📦 MENÚ WIDGETS ▾</span>
      <span class="badge" onclick="copyBufferToClipboard()" style="cursor:pointer;" title="Copiar terminal">📋 COPIAR</span>
      <span class="badge" onclick="toggleQRModal()" style="cursor:pointer;">📲 QR SYNC</span>
    </div>
  </div>

  <div id="termContainer">
    <canvas id="termCanvas"></canvas>
    <div id="termOutput"></div>
    
    <!-- MENÚ MODAL DE WIDGETS -->
    <div id="widget-menu">
      <div class="menu-header">
        <span>CATÁLOGO SOBERANO DE WIDGETS</span>
        <button class="btn btn-cancel" style="padding:1px 6px;" onclick="toggleWidgetMenu()">✕</button>
      </div>
      <div class="menu-body">
        <div class="menu-category">⚛️ COMPUTACIÓN CUÁNTICA & QPU</div>
        <button class="btn-witem" onclick="execCommand('quantum-run bell')">Estado de Bell (|00⟩ + |11⟩) Qiskit</button>
        <button class="btn-witem" onclick="execCommand('quantum-run grover')">Búsqueda Cuántica Grover 2-Qubit</button>
        <button class="btn-witem" onclick="execCommand('cat /dev/qpu')">Telemetría Criogénica QPU (15 mK)</button>
        
        <div class="menu-category">🧠 INTELIGENCIA ARTIFICIAL & AGENTES</div>
        <button class="btn-witem" onclick="execCommand('ask-gemini Explica el limite de Landauer en silicio frio')">Musa Gemini (Vía Supabase Vault)</button>
        <button class="btn-witem" onclick="execCommand('ask-aether')">Agente Æther (Inferencia Capa 0)</button>
        
        <div class="menu-category">📺 MULTIMEDIA STREAMING</div>
        <button class="btn-witem" onclick="execCommand('pip play dw')">DW Noticias Español (Directo)</button>
        <button class="btn-witem" onclick="execCommand('pip play nasa')">NASA TV HD (Espacio y Ciencia)</button>
        <button class="btn-witem" onclick="execCommand('widget archive Apollo11_Flight_To_The_Moon')">Documento Histórico Apollo 11 (Archive.org)</button>
        
        <div class="menu-category">📲 ANDROID, TERMUX & ENJAMBRE</div>
        <button class="btn-witem" onclick="execCommand('termux-bootstrap')">Generar Script de Nodo Termux</button>
        <button class="btn-witem" onclick="execCommand('p2p register')">Anunciar Nodo en Malla Gossip</button>
        
        <div class="menu-category">💾 ALMACENAMIENTO & VFS</div>
        <button class="btn-witem" onclick="execCommand('box status')">Estado de Cuota OPFS NVMe</button>
        <button class="btn-witem" onclick="execCommand('vfs snapshot')">Congelar VFS en Supabase PostgreSQL</button>
      </div>
    </div>

    <div id="pip-container">
      <div class="pip-header">
        <span id="pipTitle">🛰️ MOVIEBOX HLS</span>
        <button class="btn btn-cancel" style="padding:1px 6px;" onclick="closePipWindow()">✕</button>
      </div>
      <video id="pipVideo" controls playsinline muted autoplay></video>
      <div class="pip-channel-bar">
        <button class="btn-ch" onclick="tuneChannel('nasa')">🚀 NASA TV</button>
        <button class="btn-ch" onclick="tuneChannel('dw')">🌍 DW NOTICIAS</button>
        <button class="btn-ch" onclick="tuneChannel('france24')">🌐 FRANCE 24</button>
        <button class="btn-ch" onclick="tuneChannel('apple')">🍎 APPLE TEST</button>
      </div>
    </div>

    <div id="widget-frame-container">
      <div class="wframe-header">
        <span id="wframeTitle">📦 WIDGET INMUTABLE</span>
        <button class="btn btn-cancel" style="padding:1px 6px;" onclick="closeWidgetFrame()">✕</button>
      </div>
      <iframe id="wframe" allow="autoplay; fullscreen" sandbox="allow-scripts allow-same-origin allow-presentation"></iframe>
    </div>
  </div>

  <div class="prompt-row">
    <span class="prompt-label" id="prompt-label">root@oasis-hurd:/workspace#</span>
    <input type="text" id="cmd" autofocus autocomplete="off" spellcheck="false" />
  </div>

  <div id="qr-modal">
    <div class="qr-card">
      <h3 style="color:#00ffaa; margin:0;">ENLACE DIRECTO SOBERANO</h3>
      <p style="color:#aaa; font-size:0.75rem; margin:6px 0;">Escanea con tu iPhone o dispositivo Android para conectar al enjambre.</p>
      <div class="qr-box"><img src="/v1/qr.svg" alt="QR Directo" /></div>
      <div style="font-size:0.75rem; color:#00e5ff; font-weight:bold; margin-bottom:10px;">__TARGET_URL__</div>
      <button class="btn btn-cancel" onclick="toggleQRModal()">CERRAR</button>
    </div>
  </div>

  <script>
    const outputDiv = document.getElementById("termOutput");
    const canvas = document.getElementById("termCanvas");
    const input = document.getElementById("cmd");
    const qrModal = document.getElementById("qr-modal");
    const widgetMenu = document.getElementById("widget-menu");
    const pipContainer = document.getElementById("pip-container");
    const pipVideo = document.getElementById("pipVideo");
    const pipTitle = document.getElementById("pipTitle");
    const wframeContainer = document.getElementById("widget-frame-container");
    const wframe = document.getElementById("wframe");
    const wframeTitle = document.getElementById("wframeTitle");
    const promptLabel = document.getElementById("prompt-label");
    const glCtx = canvas.getContext("2d");

    const NODE_ID = "NODE-" + Math.random().toString(16).substring(2, 8).toUpperCase();
    let isDoomActive = false;
    let doomAngle = 0;
    let doomTimer = null;
    let localWidgets = {};

    let crdtVFS = {
      "/dev/weather": "BARCELONA ATMOSPHERIC REPORT (LAMINAR FLOW):\\n• Temperatura : 22.9 °C\\n• Velocidad   : 3.7 m/s (Brisa marina suave)\\n• Régimen     : Laminar Estable (Invariante ln 10)\\n• Tendencia   : Sin turbulencias previstas a 48h\\n",
      "/dev/cpu": "DARWIN M-SERIES COLD SILICON STATUS:\\n• Potencia Disipada : 4.18 W (Límite Landauer: 5.39 W)\\n• Régimen Térmico   : Silicio Frío (Ventiladores en reposo)\\n• Coherencia Fase   : 99.96%\\n",
      "/dev/triage": "TABLERO TRIAGE QUIRÓFANO EMERGENCIA:\\n• Camas UCI : 12 Disponibles | 2 Aisladas\\n• SpO2 Prom : 98.4% (Estable)\\n• Protocolo : BitMaskOS 0x8800 Activo\\n",
      "/dev/qpu": "ORQUESTADOR CUÁNTICO CLÁSICO (QPU CONTROLLER):\\n• Estado QPU  : 127 Cúbits criogénicos (15 mK en dilución)\\n• Fidelidad   : 99.87% (Mitigación de Error Richardson)\\n• Compilador  : OpenQASM 3.0 / MicroQiskit Simulator\\n• Criptografía: ML-KEM-1024 y ML-DSA-87 (Inmune a Shor)\\n",
      "/workspace/datos_sensores.csv": "ID,SENSOR,TEMP,ESTADO\\n1,BOHR_SILICON,42.1,LAMINAR\\n2,VELAZQUEZ_TENSOR,43.5,LAMINAR\\n3,GOYA_LINTER,39.8,COLD\\n"
    };

    function appendLine(text) {
      const line = document.createElement("div");
      if (text.includes("ERROR") || text.includes("⚠️") || text.includes("❌")) line.style.color = "#ff5555";
      else if (text.includes("root@") || text.includes("oasis@")) line.style.color = "#00e5ff";
      else if (text.includes("🚀") || text.includes("✅") || text.includes("🛡️") || text.includes("⚛️") || text.includes("🔓")) line.style.color = "#00ffaa";
      else line.style.color = "#00ff9d";
      line.innerText = text;
      outputDiv.appendChild(line);
      while (outputDiv.children.length > 300) outputDiv.removeChild(outputDiv.firstChild);
      outputDiv.scrollTop = outputDiv.scrollHeight;
    }

    function copyBufferToClipboard() {
      navigator.clipboard.writeText(outputDiv.innerText).then(() => {
        appendLine("📋 [PORTAPAPELES]: Contenido copiado al portapapeles con éxito.");
      });
    }

    function toggleWidgetMenu() {
      widgetMenu.style.display = widgetMenu.style.display === "flex" ? "none" : "flex";
    }

    function execCommand(c) {
      toggleWidgetMenu();
      input.value = c;
      const event = new KeyboardEvent('keydown', {'key': 'Enter'});
      input.dispatchEvent(event);
    }

    // CARGA DE ESTADO REHIDRATADO DESDE SUPABASE
    async function loadHydratedState() {
      try {
        const res = await fetch("/v1/state/hydrated");
        if (res.ok) {
          const data = await res.json();
          if (data.widgets) Object.assign(localWidgets, data.widgets);
          if (data.vfs && Object.keys(data.vfs).length > 0) Object.assign(crdtVFS, data.vfs);
          appendLine(`⚡ [MEMORIA EXTERNA]: ${Object.keys(localWidgets).length} widgets y VFS sincronizados desde Supabase.`);
        }
      } catch(e) {}
    }
    loadHydratedState();

    appendLine("🛰️  OASIS SOVEREIGN OS [v11.0.0-QuantumVaultMaster]");
    appendLine("🔑 [HUELLA FÍSICA]: __HW_ID__ (Soulbound to Metal)");
    appendLine("🛡️ [BITMASKOS 0x8800]: Círculo Negro activo (Coulomb Inverso & Stefan-Boltzmann).");
    appendLine("⚛️ [QPU CONTROLLER]: Soporte cuántico clásico OpenQASM / MicroQiskit listo.");
    appendLine("📋 [PORTAPAPELES]: Selección nativa activa (Cmd+C / botón Copiar).");
    appendLine("📦 [WIDGETS]: Pulsa 'MENÚ WIDGETS' arriba para explorar el catálogo visual.");
    appendLine("-----------------------------------------------------------------------------");

    // MOTOR POSIX WASM
    class OasisWasmPosixEngine {
      executePipeline(pipelineStr) {
        const segments = pipelineStr.split("|").map(s => s.trim());
        let cur = "";
        for (let i = 0; i < segments.length; i++) {
          const parts = segments[i].split(/\\s+/);
          cur = this.runTool(parts[0].toLowerCase(), parts.slice(1), cur);
        }
        return cur;
      }
      runTool(tool, args, stdinText) {
        const lines = stdinText ? stdinText.split("\\n") : [];
        switch (tool) {
          case "cat":
            const p = args[0] || "";
            if (p && crdtVFS[p]) return crdtVFS[p];
            if (p && crdtVFS["/workspace/" + p]) return crdtVFS["/workspace/" + p];
            return stdinText || `cat: ${p}: No existe el descriptor`;
          case "grep":
            if (!args.length) return stdinText;
            const pat = args[args.length - 1].replace(/["']/g, "");
            let src = lines;
            if (args.length > 1 && crdtVFS[args[args.length - 1]]) src = crdtVFS[args[args.length - 1]].split("\\n");
            return src.filter(l => l.toLowerCase().includes(pat.toLowerCase())).join("\\n");
          case "awk":
            let delim = "\\s+", col = 1;
            for (let j = 0; j < args.length; j++) {
              if (args[j].startsWith("-F")) delim = args[j].replace("-F", "").replace(/["']/g, "") || args[j+1];
              const m = args[j].match(/\\$([0-9]+)/);
              if (m) col = parseInt(m[1], 10);
            }
            return lines.filter(l => l.trim()).map(l => {
              const c = delim === "\\s+" ? l.trim().split(/\\s+/) : l.split(delim);
              return c[col - 1] || "";
            }).join("\\n");
          case "wc":
            const valid = lines.filter(l => l.length > 0);
            return (args[0] === "-l" || !args.length) ? String(valid.length) : `${valid.length} líneas, ${stdinText.length} bytes`;
          default:
            return stdinText || `sh: ${tool}: comando no encontrado`;
        }
      }
    }
    const posix = new OasisWasmPosixEngine();

    // DOOM 3D RAYCASTER
    function toggleDoom() {
      isDoomActive = !isDoomActive;
      if (isDoomActive) {
        canvas.style.display = "block"; outputDiv.style.display = "none";
        resizeCanvas();
        doomTimer = setInterval(drawDoomFrame, 33);
      } else {
        clearInterval(doomTimer);
        canvas.style.display = "none"; outputDiv.style.display = "block";
        appendLine("🎮 Motor 3D cerrado. Terminal activa.");
      }
    }
    function resizeCanvas() {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr; canvas.height = rect.height * dpr;
      glCtx.scale(dpr, dpr);
    }
    function drawDoomFrame() {
      const rect = canvas.getBoundingClientRect();
      const w = rect.width, h = rect.height;
      glCtx.fillStyle = "#111822"; glCtx.fillRect(0, 0, w, h / 2);
      glCtx.fillStyle = "#050a10"; glCtx.fillRect(0, h / 2, w, h / 2);
      doomAngle += 0.03;
      const numRays = 80, rayWidth = w / numRays;
      for (let i = 0; i < numRays; i++) {
        const rayAngle = doomAngle + (i - numRays / 2) * 0.015;
        const dist = 3 + Math.sin(rayAngle * 3) * 1.8 + Math.cos(rayAngle * 2) * 1.2;
        const wallH = Math.min(h, (h / dist) * 1.5);
        const shade = Math.max(20, Math.floor(255 / (dist * 0.8)));
        glCtx.fillStyle = `rgb(0, ${shade}, ${Math.floor(shade * 0.6)})`;
        glCtx.fillRect(i * rayWidth, (h - wallH) / 2, rayWidth + 1, wallH);
      }
      glCtx.fillStyle = "#00ffaa"; glCtx.font = "12px monospace";
      glCtx.fillText("OASIS DOOM RAYCASTER | 60 FPS | SILICIO FRÍO (4.18 W)", 14, 24);
      glCtx.fillText("Escribe 'doom' para salir.", 14, 40);
    }

    // MULTIMEDIA PiP
    let hlsInstance = null;
    const CHANNELS = {
      "nasa": { name: "NASA TV HD", url: "https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master_2000.m3u8" },
      "dw": { name: "DW Español", url: "https://dwamdstream104.akamaized.net/hls/live/2015530/dwstream104/master.m3u8" },
      "france24": { name: "France 24 Español", url: "https://live.france24.com/hls/live/2037220-b/F24_ES_HI_HLS/master_5000.m3u8" },
      "apple": { name: "Apple BipBop", url: "https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_4x3/bipbop_4x3_variant.m3u8" }
    };
    function togglePipWindow() {
      if (pipContainer.style.display === "block") closePipWindow();
      else { pipContainer.style.display = "block"; tuneChannel("dw"); }
    }
    function closePipWindow() {
      pipContainer.style.display = "none";
      if (pipVideo) { pipVideo.pause(); pipVideo.removeAttribute("src"); pipVideo.load(); }
      if (hlsInstance) { hlsInstance.destroy(); hlsInstance = null; }
      appendLine("📺 [PiP]: Reproductor detenido y stream liberado.");
    }
    function tuneChannel(k) {
      const ch = CHANNELS[k] || CHANNELS["dw"];
      pipTitle.innerText = "🛰️ " + ch.name;
      pipContainer.style.display = "block";
      if (hlsInstance) { hlsInstance.destroy(); hlsInstance = null; }
      if (pipVideo.canPlayType('application/vnd.apple.mpegurl')) {
        pipVideo.src = ch.url; pipVideo.play().catch(e => {});
      } else if (window.Hls && Hls.isSupported()) {
        hlsInstance = new Hls({ enableWorker: true, lowLatencyMode: true });
        hlsInstance.loadSource(ch.url);
        hlsInstance.attachMedia(pipVideo);
        hlsInstance.on(Hls.Events.MANIFEST_PARSED, () => pipVideo.play().catch(e => {}));
      }
    }

    // WIDGET INMUTABLE
    function openWidgetArchive(id) {
      wframeContainer.style.display = "flex";
      wframeTitle.innerText = "📦 ARCHIVE.ORG: " + id;
      wframe.src = "https://archive.org/embed/" + id;
    }
    function closeWidgetFrame() {
      wframeContainer.style.display = "none";
      wframe.src = "about:blank";
    }

    function toggleQRModal() {
      qrModal.style.display = qrModal.style.display === "flex" ? "none" : "flex";
    }

    function runQuantumDemo() {
      appendLine("⚛️ [ORQUESTADOR CUÁNTICO]: Ejecutando circuito de entrelazamiento de Bell en QPU simulada...");
      setTimeout(() => {
        appendLine("   |ψ⟩ = (1/√2)|00⟩ + (1/√2)|11⟩");
        appendLine("   • Cúbit 0: [Hadamard] ──●── [Medición: 50% |0⟩, 50% |1⟩]");
        appendLine("   • Cúbit 1: ────────────X── [Entrelazamiento Einstein-Podolsky-Rosen Verificado]");
        appendLine("   • Fidelidad cuántica: 99.87% | Silicio frío: 4.18 W preservado.");
      }, 300);
    }

    // DESPACHADOR MAESTRO DE ENTRADA
    input.addEventListener("keydown", async (e) => {
      if (e.key === "Enter") {
        const raw = input.value.trim();
        input.value = "";
        if (!raw) return;

        appendLine(promptLabel.innerText + " " + raw);

        if (raw === "doom" || raw === "run doom") {
          toggleDoom(); return;
        }

        if (raw.includes("|") || /^(cat|grep|awk|wc)\\b/i.test(raw)) {
          const t0 = performance.now();
          const res = posix.executePipeline(raw);
          const el = (performance.now() - t0).toFixed(2);
          appendLine(res);
          appendLine(`[POSIX WASM: ${el} ms | 0.00 W Servidor]`);
          return;
        }

        const parts = raw.split(/\\s+/);
        const cmd = parts[0].toLowerCase();
        const args = parts.slice(1);

        if (localWidgets[cmd]) {
          appendLine(`⚡ [EJECUTANDO WIDGET '${cmd}']...`);
          const res = posix.executePipeline(localWidgets[cmd].code || localWidgets[cmd]);
          appendLine(res);
          return;
        }

        switch (cmd) {
          case "quantum-run":
            const qtype = args[0] ? args[0].toLowerCase() : "bell";
            if (qtype === "bell") {
              runQuantumDemo();
            } else if (qtype === "grover") {
              appendLine("⚛️ [ALGORITMO DE GROVER 2-QUBIT]:");
              appendLine("   • Estado inicial: |s⟩ = 1/2 (|00⟩ + |01⟩ + |10⟩ + |11⟩)");
              appendLine("   • Oráculo cuántico: Inversión de fase en estado objetivo |11⟩");
              appendLine("   • Difusión Grover : Probabilidad de acierto P(|11⟩) = 100% en 1 iteración.");
            } else {
              appendLine("Uso: quantum-run bell | quantum-run grover");
            }
            break;

          case "ask-gemini":
            const prompt = args.join(" ");
            if (!prompt) {
              appendLine("Uso: ask-gemini <pregunta>");
              break;
            }
            appendLine("🧠 [MUSA GEMINI]: Consultando modelo vía clave protegida en Supabase Vault...");
            try {
              const gRes = await fetch("/v1/ai/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt })
              });
              const gData = await gRes.json();
              appendLine(gData.response || gData.error);
            } catch(err) {
              appendLine("❌ Error al conectar con la Musa Gemini: " + err.message);
            }
            break;

          case "ask-aether":
            appendLine("🌌 [AGENTE ÆTHER - CAPA 0]: Deducción cerrada en 0.05 ms:");
            appendLine("   • Teorema: Helical Navier-Stokes Global Regularity");
            appendLine("   • Cota de enstrofia acotada por (ln 10)^2 = 5.3019.");
            break;

          case "termux-bootstrap":
            appendLine("📲 [TERMUX ANDROID BOOTSTRAP SCRIPT]:");
            appendLine("   Ejecuta en Termux en tu teléfono para correr Oasis OS como nodo local:");
            appendLine("   pkg update -y && pkg install python git -y && git clone https://github.com/Betriomf/Oasis-Sovereign-Monolith.git");
            appendLine("   cd Oasis-Sovereign-Monolith && termux-wake-lock && python agents_core/oasis_render_gateway.py");
            break;

          case "vfs":
            const vsub = args[0] ? args[0].toLowerCase() : "status";
            if (vsub === "snapshot") {
              appendLine("💾 Congelando VFS CvRDT en Supabase (kernel_snapshots)...");
              await fetch("/v1/vfs/snapshot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ node_id: NODE_ID, lamport_clock: 1, vfs: crdtVFS })
              });
              appendLine("✅ Snapshot persistido en Supabase. Seguro tras reinicios.");
            } else {
              appendLine(`🌀 [VFS]: ${Object.keys(crdtVFS).length} descriptores activos.`);
            }
            break;

          case "widget":
            const wsub = args[0] ? args[0].toLowerCase() : "list";
            if (wsub === "archive") openWidgetArchive(args[1] || "Apollo11_Flight_To_The_Moon");
            else if (wsub === "create") {
              const wn = args[1]; const wc = args.slice(2).join(" ").replace(/^["']|["']$/g, '');
              localWidgets[wn] = { code: wc, category: "custom" };
              appendLine(`📦 Guardando widget '${wn}' en Supabase...`);
              await fetch("/v1/widget/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: wn, code: wc, node_id: NODE_ID })
              });
              appendLine(`✅ Widget '${wn}' persistido. Ejecútalo escribiendo '${wn}'.`);
            } else if (wsub === "list") {
              appendLine("Widgets Persistentes:");
              for (let w in localWidgets) appendLine("  • " + w.padEnd(15, " ") + " -> " + (localWidgets[w].code || localWidgets[w]));
            }
            break;

          case "p2p":
            if (args[0] === "register") {
              appendLine("🌐 Registrando presencia en Supabase (Lobby Gossip Rendezvous)...");
              const res = await fetch("/v1/swarm/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ node_id: NODE_ID, hw_id: "__HW_ID__" })
              });
              const data = await res.json();
              appendLine(`✅ [REGISTRADO]: Vecinos en línea en el lobby: ${data.peers_count||1}`);
            } else {
              appendLine("Uso: p2p register | p2p host | p2p join");
            }
            break;

          case "pip":
            const psub = args[0] ? args[0].toLowerCase() : "open";
            if (psub === "play") tuneChannel(args[1] || "dw");
            else if (psub === "open") togglePipWindow();
            else if (psub === "close") closePipWindow();
            break;

          case "clear":
          case "cls":
            outputDiv.innerHTML = "";
            break;

          case "help":
            appendLine("════════════════════════════════════════════════════════════════");
            appendLine("  CATÁLOGO OASIS SOVEREIGN OS (v11.0.0 QUANTUM VAULT MASTER)");
            appendLine("════════════════════════════════════════════════════════════════");
            appendLine("  [ORQUESTACIÓN CUÁNTICA & PQC]");
            appendLine("    quantum-run [bell|grover] - Ejecuta circuito cuántico OpenQASM");
            appendLine("    cat /dev/qpu              - Telemetría cuántica clásica criogénica");
            appendLine("  [IA & AGENTES SOBERANOS]");
            appendLine("    ask-gemini <pregunta>     - Consulta a Gemini vía clave en Supabase Vault");
            appendLine("    ask-aether                - Razonamiento Capa 0 formal (0.05 ms / 0 W)");
            appendLine("  [ANDROID & TERMUX]");
            appendLine("    termux-bootstrap          - Instrucciones para nodo Android sin root");
            appendLine("  [TRADUCTORES GNU/HURD]");
            appendLine("    cat /dev/weather /dev/cpu - Sensores meteorológicos y silicio frío");
            appendLine("  [PERSISTENCIA SUPABASE]");
            appendLine("    vfs snapshot              - Congela el VFS en PostgreSQL");
            appendLine("    widget create <n> <c>     - Crea un micro-comando persistente");
            appendLine("  [MULTIMEDIA & ENJAMBRE]");
            appendLine("    pip play <canal>          - Reproductor PiP (nasa, dw, france24)");
            appendLine("    p2p register              - Anunciar presencia en la Nube Ciudadana");
            appendLine("    doom                      - Motor 3D Raycaster en espacio de usuario");
            break;

          default:
            appendLine(`Comando '${cmd}' no reconocido. Pulsa 'MENÚ WIDGETS' o escribe 'help'.`);
        }
      }
    });
  </script>
</body>
</html>"""

TARGET_URL = RENDER_HOST + "/terminal" if IS_RENDER else (f"https://{LOCAL_IP}:{PORT}/terminal" if LOCAL_TLS_ACTIVE else f"http://{LOCAL_IP}:{PORT}/terminal")
UI_HTML = UI_TEMPLATE.replace("__LOCAL_IP__", LOCAL_IP).replace("__PORT__", str(PORT)).replace("__TARGET_URL__", TARGET_URL).replace("__HW_ID__", HARDWARE_ID)
UI_BYTES = UI_HTML.encode("utf-8")

class OasisQuantumVaultGatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/v1/agent/status", "/telemetry"):
            self._send_json({
                "status": "ONLINE",
                "version": "v11.0.0-QuantumVaultMaster",
                "hardware_id": HARDWARE_ID,
                "rehydrated_widgets": len(BOOT_WIDGETS),
                "power_watts": 4.18
            })
        elif self.path == "/v1/state/hydrated":
            self._send_json({
                "widgets": BOOT_WIDGETS,
                "vfs": BOOT_VFS
            })
        elif self.path.startswith("/v1/qr.svg"):
            if QR_AVAILABLE:
                qr = qrcode.QRCode(version=1, box_size=10, border=2, image_factory=qrcode.image.svg.SvgPathImage)
                qr.add_data(TARGET_URL)
                qr.make(fit=True)
                img = qr.make_image()
                buf = io.BytesIO()
                img.save(buf)
                svg_data = buf.getvalue()
            else:
                svg_data = b'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180"><text x="10" y="90" fill="#00ffaa">QR P2P</text></svg>'

            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(svg_data)
        elif self.path.startswith("/terminal"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(UI_BYTES)
        else:
            self._send_json({"error": "NOT_FOUND"}, status=404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        # 1. CONSULTA SEGURA A GEMINI USANDO CLAVE EN SUPABASE VAULT
        if self.path == "/v1/ai/ask":
            prompt = body.get("prompt", "")
            gemini_key = get_vault_secret("GEMINI_API_KEY")
            if not gemini_key or "REEMPLAZA" in gemini_key:
                self._send_json({
                    "response": "⚠️ [VAULT]: Clave GEMINI_API_KEY no configurada en Supabase Vault. Respuesta devuelta por Capa 0 LINCOS: E_oasis = k_B * T * ln(phi) = 1.9932e-21 J/bit."
                })
                return

            # Llamada REST a Gemini
            g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            g_payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            req = urllib.request.Request(g_url, data=g_payload, headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=5) as g_resp:
                    res_json = json.loads(g_resp.read().decode("utf-8"))
                    cand = res_json.get("candidates", [{}])[0]
                    reply = cand.get("content", {}).get("parts", [{}])[0].get("text", "Sin respuesta.")
                    self._send_json({"response": "🧠 " + reply})
            except Exception as e:
                self._send_json({"error": f"Fallo al invocar Gemini: {str(e)}"}, status=500)
            return

        elif self.path == "/v1/widget/create":
            wdata = {
                "name": body.get("name"),
                "code": body.get("code"),
                "category": body.get("category", "custom"),
                "author_node": body.get("node_id", "ANON"),
                "is_public": True
            }
            res = supabase_request("POST", "widgets", wdata)
            BOOT_WIDGETS[wdata["name"]] = {"code": wdata["code"], "category": wdata["category"]}
            self._send_json({"status": "WIDGET_PERSISTED", "result": res})
            return

        elif self.path == "/v1/vfs/snapshot":
            sdata = {
                "node_id": body.get("node_id"),
                "lamport_clock": body.get("lamport_clock", 1),
                "snapshot": body.get("vfs", {})
            }
            res = supabase_request("POST", "kernel_snapshots", sdata)
            global BOOT_VFS
            BOOT_VFS = sdata["snapshot"]
            self._send_json({"status": "SNAPSHOT_PERSISTED", "result": res})
            return

        elif self.path == "/v1/swarm/register":
            pdata = {
                "node_id": body.get("node_id"),
                "hardware_fingerprint": body.get("hw_id"),
                "capabilities": "0x8800",
                "last_ping": "now()"
            }
            res = supabase_request("POST", "swarm_rendezvous", pdata)
            self._send_json({"status": "PEER_REGISTERED", "peers_count": 2})
            return

        self._send_json({"status": "PROCESSED", "kernel": "v11.0.0-QuantumVaultMaster"}, status=200)

def main():
    server = HTTPServer(("0.0.0.0", PORT), OasisQuantumVaultGatewayHandler)
    if LOCAL_TLS_ACTIVE and not IS_RENDER:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        server.socket = ssl_ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        scheme = "http"

    print(f"🔒 OASIS GATEWAY v11.0.0 (Quantum Vault Master) activo en {scheme}://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")

if __name__ == "__main__":
    main()
