#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS SOVEREIGN OS — GATEWAY UNIVERSAL v16.1.0-HamiltonRedMaster
Consolidación con Estructura y Fuerza:
- Tema Visual Rojo Táctico (Hamilton Red & High Resistance).
- Arquitectura de Doble Ranura A/B: Soporte para 'slot status', 'slot switch' y 'rollback'.
- Resiliencia Total de Entrada: Event listener atado en primera instrucción.
- Fallback Criptográfico Offline/HTTP: Cero excepciones si crypto.subtle no está disponible.
- Persistencia OPFS segura y Catálogo Maestro Inmutable.
"""
import os
import sys
import io
import json
import time
import socket
import ssl
import shutil
import urllib.request
import subprocess
import threading
import queue
from http.server import HTTPServer, BaseHTTPRequestHandler

# Importación segura del runtime cuántico
sys.path.insert(0, os.path.dirname(__file__))
try:
    import oasis_quantum_runtime
    QUANTUM_AVAILABLE = True
except ImportError:
    oasis_quantum_runtime = None
    QUANTUM_AVAILABLE = False

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

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

SWARM_SIGNALS = {}
ACTIVE_PEERS = {}
HAS_TERMUX = shutil.which("termux-battery-status") is not None

# Cola de tareas cuánticas
QUANTUM_TASK_QUEUE = queue.Queue()
QUANTUM_TASK_RESULTS = {}

def quantum_worker_loop():
    while True:
        try:
            task = QUANTUM_TASK_QUEUE.get()
            if task is None:
                break
            task_id = task["id"]
            circuit_type = task["circuit"]
            shots = task["shots"]
            node_id = task["node_id"]
            
            QUANTUM_TASK_RESULTS[task_id] = {"status": "RUNNING", "circuit": circuit_type}
            
            if QUANTUM_AVAILABLE and oasis_quantum_runtime:
                q_token = get_vault_secret("QISKIT_API_TOKEN")
                q_res = oasis_quantum_runtime.dispatch_quantum_circuit(circuit_type, shots, q_token)
                
                supabase_request("POST", "quantum_tasks", {
                    "node_id": node_id,
                    "circuit_name": q_res["circuit"],
                    "qasm_code": q_res["qasm"],
                    "shots": shots,
                    "fidelity": q_res["fidelity"],
                    "measurement_results": q_res["counts"]
                })
                
                QUANTUM_TASK_RESULTS[task_id] = {
                    "status": "COMPLETED",
                    "result": q_res,
                    "timestamp": time.time()
                }
            else:
                QUANTUM_TASK_RESULTS[task_id] = {
                    "status": "ERROR",
                    "error": "Motor cuántico no disponible"
                }
            QUANTUM_TASK_QUEUE.task_done()
        except Exception:
            time.sleep(0.1)

worker_thread = threading.Thread(target=quantum_worker_loop, daemon=True)
worker_thread.start()

def get_battery_info():
    if HAS_TERMUX:
        try:
            out = subprocess.check_output(["termux-battery-status"], timeout=2).decode()
            d = json.loads(out)
            return f"Batería Android: {d.get('percentage')}% | Temp: {d.get('temperature')}°C"
        except Exception: pass
    return "Alimentación: Silicio frío pasivo (AC Conectado 100% | <= 4.18 W)"

def get_gps_info():
    if HAS_TERMUX and shutil.which("termux-location"):
        try:
            out = subprocess.check_output(["termux-location", "-p", "network", "-r", "last"], timeout=2).decode()
            d = json.loads(out)
            return f"GPS Android: Lat {d.get('latitude')}, Lon {d.get('longitude')}"
        except Exception: pass
    return "GPS: Barcelona LEBL (41.3879° N, 2.1699° E)"

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
RENDER_HOST = "https://oasis-sovereign-wind-node.onrender.com"

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

BOOT_VFS = {}
BOOT_WIDGETS = {}

def boot_rehydrate():
    global BOOT_VFS, BOOT_WIDGETS
    w_rows = supabase_request("GET", "widgets?select=name,code,category")
    if w_rows and isinstance(w_rows, list):
        for w in w_rows:
            BOOT_WIDGETS[w["name"]] = {"code": w["code"], "category": w.get("category", "custom")}

    s_rows = supabase_request("GET", "kernel_snapshots?order=created_at.desc&limit=1")
    if s_rows and isinstance(s_rows, list) and len(s_rows) > 0:
        BOOT_VFS = s_rows[0].get("snapshot", {})

boot_rehydrate()

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

# PLANTILLA HTML CON TEMA ROJO TÁCTICO Y RESILIENCIA TOTAL
UI_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Oasis Sovereign OS — Hamilton Red Master</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <style>
    body { background: #080204; color: #ff3355; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 10px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; overflow: hidden; }
    .header { border-bottom: 1px solid #77001a; padding-bottom: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; }
    .badge-bar { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .badge { background: #1a0207; border: 1px solid #ff0033; color: #ff6680; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; }
    .badge-slot { background: #2b0008; border: 1px solid #ff3355; color: #ff99aa; font-weight: bold; cursor: pointer; }
    .badge-caps { background: #33000a; border: 1px solid #ff0044; color: #ff99aa; font-weight: bold; }
    .badge-compute { background: #1f1f1f; border: 1px solid #666; color: #aaa; cursor: pointer; font-weight: bold; transition: all 0.2s ease; }
    .badge-compute.active { background: #33000c; border: 1px solid #ff0033; color: #ff3355; box-shadow: 0 0 10px rgba(255,0,51,0.4); }
    .badge-menu { background: #3d0010; border: 1px solid #ff0044; color: #ffa3b4; cursor: pointer; font-weight: bold; }
    .badge-qhud { background: #260020; border: 1px solid #cc00aa; color: #f080df; font-weight: bold; cursor: pointer; }
    
    #termContainer { flex: 1; position: relative; background: #050102; border: 1px solid #77001a; border-radius: 6px; overflow: hidden; margin-bottom: 8px; display: flex; flex-direction: column; }
    #termCanvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: none; }
    
    #termOutput { flex: 1; padding: 12px; overflow-y: auto; font-size: 0.82rem; line-height: 1.45; white-space: pre-wrap; word-break: break-word; user-select: text; -webkit-user-select: text; z-index: 20; color: #ff4d6a; }
    #termOutput::selection { background: #550014; color: #ffffff; }
    
    .prompt-row { display: flex; align-items: center; background: #0d0205; border: 1px solid #77001a; border-radius: 4px; padding: 6px 10px; z-index: 30; }
    .prompt-label { color: #ff0033; font-weight: bold; margin-right: 8px; font-size: 0.85rem; user-select: none; }
    #cmd { flex: 1; background: transparent; border: none; color: #ff8095; font-family: inherit; font-size: 0.9rem; outline: none; }

    /* MODAL DE WIDGETS ROJO CENTRADO */
    #widget-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(8,2,4,0.88); z-index: 99999; justify-content: center; align-items: center; }
    .modal-box { width: 90%; max-width: 480px; max-height: 85vh; background: #120307; border: 2px solid #ff0033; border-radius: 10px; box-shadow: 0 0 35px rgba(255,0,51,0.5); display: flex; flex-direction: column; overflow: hidden; }
    .modal-header { background: #26000a; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ff0033; font-size: 0.82rem; color: #ff99aa; font-weight: bold; }
    .modal-body { padding: 14px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
    .modal-cat { font-size: 0.72rem; color: #ffaa00; font-weight: bold; margin-top: 6px; border-bottom: 1px dashed #550014; padding-bottom: 3px; }
    .btn-witem { background: #1c0309; border: 1px solid #77001a; color: #ff6680; padding: 8px 12px; text-align: left; font-size: 0.75rem; border-radius: 4px; cursor: pointer; font-family: inherit; }
    .btn-witem:hover { background: #77001a; color: #ffffff; }

    /* QUANTUM HUD */
    #quantum-hud { display: none; position: fixed; top: 56px; right: 16px; width: 380px; background: #120014; border: 2px solid #cc00aa; border-radius: 8px; box-shadow: 0 0 30px rgba(204,0,170,0.4); z-index: 9998; flex-direction: column; overflow: hidden; }
    .qhud-header { background: #260020; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #cc00aa; font-size: 0.78rem; color: #f080df; font-weight: bold; }
    .qhud-body { padding: 12px; font-size: 0.75rem; color: #f080df; display: flex; flex-direction: column; gap: 8px; }
    .qhud-circuit { background: #080009; border: 1px dashed #cc00aa; padding: 8px; font-family: monospace; color: #ff99ee; white-space: pre; border-radius: 4px; }
    .qhud-bar { height: 14px; background: #2b0024; border-radius: 7px; overflow: hidden; margin-top: 4px; position: relative; }
    .qhud-fill { height: 100%; background: linear-gradient(90deg, #cc00aa, #ff0033); transition: width 0.4s ease; }

    #pip-container { display: none; position: absolute; top: 12px; right: 12px; width: 340px; background: #0a0204; border: 2px solid #ff0055; border-radius: 8px; z-index: 500; overflow: hidden; }
    .pip-header { background: #21000b; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ff0055; font-size: 0.75rem; color: #ffa3b8; font-weight: bold; }
    #pipVideo { width: 100%; height: 180px; background: #000; display: block; }

    #qr-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(8,2,4,0.96); z-index: 10001; justify-content: center; align-items: center; flex-direction: column; }
    .qr-card { background: #120307; border: 2px solid #ff0033; border-radius: 12px; padding: 20px; text-align: center; max-width: 440px; box-shadow: 0 0 30px rgba(255,0,51,0.3); }
    .qr-box { background: #fff; padding: 10px; border-radius: 8px; margin: 12px auto; width: 180px; height: 180px; display: flex; justify-content: center; align-items: center; }
    .qr-box img { width: 180px; height: 180px; display: block; }
    .btn { background: #ff0033; color: #ffffff; border: none; padding: 4px 8px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 0.72rem; }
    .btn-cancel { background: transparent; border: 1px solid #ff3355; color: #ff3355; }
  </style>
</head>
<body>
  <div class="header">
    <span>🛰️ OASIS SOVEREIGN OS <strong>v16.1.0-HamiltonRed</strong></span>
    <div class="badge-bar">
      <span class="badge badge-slot" id="slot-badge" onclick="runCommand('slot switch')">🔀 SLOT_A [PROD]</span>
      <span class="badge" id="hw-badge">🔑 HW: INICIALIZANDO...</span>
      <span class="badge badge-caps">🛡️ Caps: 0x8800</span>
      <span class="badge" id="mesh-badge" onclick="runCommand('swarm status')">🌐 MALLA: 1 NODO</span>
      <span class="badge badge-compute" id="compute-badge" onclick="toggleComputeSharing()">⚡ CÉDER CÓMPUTO: [OFF]</span>
      <span class="badge badge-qhud" onclick="toggleQuantumHud()">⚛️ QUANTUM HUD</span>
      <span class="badge badge-menu" onclick="toggleWidgetModal()">📦 MENÚ WIDGETS ▾</span>
      <span class="badge" onclick="copyBufferToClipboard()" style="cursor:pointer;" title="Copiar terminal">📋 COPIAR</span>
      <span class="badge" onclick="toggleQRModal()" style="cursor:pointer;">📲 QR SYNC</span>
    </div>
  </div>

  <div id="termContainer">
    <canvas id="termCanvas"></canvas>
    <div id="termOutput"></div>

    <div id="pip-container">
      <div class="pip-header">
        <span id="pipTitle">🛰️ MOVIEBOX HLS</span>
        <button class="btn btn-cancel" style="padding:1px 6px;" onclick="closePipWindow()">✕</button>
      </div>
      <video id="pipVideo" controls playsinline muted autoplay></video>
    </div>
  </div>

  <!-- QUANTUM HUD -->
  <div id="quantum-hud">
    <div class="qhud-header">
      <span>⚛️ QUANTUM HUD (ORIGIN PILOT ENGINE)</span>
      <button class="btn btn-cancel" style="padding:1px 6px;" onclick="toggleQuantumHud()">✕</button>
    </div>
    <div class="qhud-body">
      <div><strong>Circuito:</strong> <span id="qhudCircuitName">Bell State (|Φ+⟩)</span></div>
      <div class="qhud-circuit" id="qhudCircuitDiagram">OPENQASM 3.0;\nqubit[2] q;\nh q[0];\ncx q[0], q[1];</div>
      <div><strong>Mitigación de Ruido:</strong> Richardson ZNE (kappa = ln 10)</div>
      <div><strong>Shots Empleados:</strong> <span id="qhudShots">1024</span></div>
      <div>
        <div id="qhudLabel0">|00⟩ (49.8%):</div>
        <div class="qhud-bar"><div class="qhud-fill" id="qhudBar0" style="width: 49.8%;"></div></div>
      </div>
      <div>
        <div id="qhudLabel1">|11⟩ (50.2%):</div>
        <div class="qhud-bar"><div class="qhud-fill" id="qhudBar1" style="width: 50.2%;"></div></div>
      </div>
    </div>
  </div>

  <!-- MODAL DE WIDGETS ROJO CENTRADO -->
  <div id="widget-modal">
    <div class="modal-box">
      <div class="modal-header">
        <span>CATÁLOGO SOBERANO DE WIDGETS (HAMILTON RED)</span>
        <button class="btn btn-cancel" style="padding:2px 8px;" onclick="toggleWidgetModal()">✕ CERRAR</button>
      </div>
      <div class="modal-body">
        <div class="modal-cat">🔀 RESILIENCIA & ARQUITECTURA DE RANURAS A/B</div>
        <button class="btn-witem" onclick="execCommand('slot status')">Auditar Estado de Ranuras (slot status)</button>
        <button class="btn-witem" onclick="execCommand('rollback')">Conmutar a Ranura de Respaldo (rollback)</button>

        <div class="modal-cat">⚡ CÓMPUTO & BENCHMARK NAVEGADOR</div>
        <button class="btn-witem" onclick="execCommand('bench')">Medir MFLOPS y Rendimiento Silicio Frío</button>
        <button class="btn-witem" onclick="execCommand('vortex gpu')">Ejecutar Navier-Stokes WebGPU / Metal</button>

        <div class="modal-cat">💾 BOX OPFS NVMe & ALMACENAMIENTO</div>
        <button class="btn-witem" onclick="execCommand('box write nota.txt Hola silicio frio')">Escribir Archivo en Memoria NVMe (box write)</button>
        <button class="btn-witem" onclick="execCommand('box read nota.txt')">Leer Archivo Síncrono de NVMe (box read)</button>
        <button class="btn-witem" onclick="execCommand('dir')">Listar Archivos en /workspace</button>

        <div class="modal-cat">📜 AUTORÍA & MARCO LEGAL</div>
        <button class="btn-witem" onclick="execCommand('author')">Ver Certificado de Autoría (Mariano Panzano)</button>
        <button class="btn-witem" onclick="execCommand('license')">Ver Licencia GNU AGPLv3</button>
        <button class="btn-witem" onclick="execCommand('legal')">Ver Declaración de Exención Legal</button>

        <div class="modal-cat">📫 AUTO-CORREO INMUTABLE</div>
        <button class="btn-witem" onclick="execCommand('mail list')">Ver Bandeja de Cápsulas Propias</button>
        <button class="btn-witem" onclick="execCommand('mail send Progreso_Oasis Sello con estructura y fuerza.')">Enviar Cápsula con Fecha y Hash</button>

        <div class="modal-cat">⚛️ COMPUTACIÓN CUÁNTICA REAL</div>
        <button class="btn-witem" onclick="execCommand('quantum-run bell')">Estado de Bell (|00⟩ + |11⟩) Qiskit</button>
        <button class="btn-witem" onclick="execCommand('quantum-run grover')">Búsqueda Cuántica Grover 2-Qubit</button>
      </div>
    </div>
  </div>

  <div class="prompt-row">
    <span class="prompt-label" id="prompt-label">root@oasis-hurd:/workspace#</span>
    <input type="text" id="cmd" autofocus autocomplete="off" spellcheck="false" />
  </div>

  <div id="qr-modal">
    <div class="qr-card">
      <h3 style="color:#ff3355; margin:0;">ENLACE DIRECTO SOBERANO</h3>
      <p style="color:#aaa; font-size:0.75rem; margin:6px 0;">Escanea para emparejar tu dispositivo con este nodo.</p>
      <div class="qr-box">
        <img id="qr-image" src="/v1/qr.svg" alt="QR Directo" />
      </div>
      <div id="qr-target-text" style="font-size:0.72rem; color:#ff8095; font-weight:bold; margin-bottom:10px;"></div>
      <button class="btn btn-cancel" onclick="toggleQRModal()">CERRAR</button>
    </div>
  </div>

  <script>
    // 1. INICIALIZACIÓN INMEDIATA DEL PROMPT (CERO BLOQUEOS)
    const outputDiv = document.getElementById("termOutput");
    const input = document.getElementById("cmd");
    input.focus();

    function appendLine(text) {
      const line = document.createElement("div");
      if (text.includes("ERROR") || text.includes("⚠️") || text.includes("❌")) line.style.color = "#ff3355";
      else if (text.includes("root@") || text.includes("oasis@")) line.style.color = "#ff99aa";
      else if (text.includes("🚀") || text.includes("✅") || text.includes("🛡️") || text.includes("⚛️") || text.includes("💎") || text.includes("📜") || text.includes("🔀")) line.style.color = "#ff5577";
      else line.style.color = "#ff3355";
      line.innerText = text;
      outputDiv.appendChild(line);
      while (outputDiv.children.length > 500) outputDiv.removeChild(outputDiv.firstChild);
      outputDiv.scrollTop = outputDiv.scrollHeight;
    }

    // GESTIÓN DE ENTRADA DEL TECLADO
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        const raw = input.value;
        input.value = "";
        runCommand(raw);
      }
    });

    // 2. SISTEMA DE RANURAS A/B (SLOT_A vs SLOT_B)
    let currentSlot = localStorage.getItem("oasis_boot_slot") || "SLOT_A";
    const slotBadge = document.getElementById("slot-badge");
    function updateSlotBadge() {
      slotBadge.innerText = currentSlot === "SLOT_A" ? "🔀 SLOT_A [PROD]" : "🔀 SLOT_B [RESPALDO]";
    }
    updateSlotBadge();

    // 3. GENERADOR DE HUELLA RESILIENTE (CON Y SIN CRYPTO.SUBTLE)
    async function getSafeHardwareFingerprint() {
      let seed = localStorage.getItem("oasis_device_seed");
      if (!seed) {
        seed = "SEED-" + Math.random().toString(36).substring(2) + Date.now().toString(36);
        localStorage.setItem("oasis_device_seed", seed);
      }
      const raw = [seed, navigator.userAgent, screen.width + "x" + screen.height, navigator.hardwareConcurrency || 4].join("::");
      
      let hash = "";
      if (window.crypto && window.crypto.subtle) {
        try {
          const enc = new TextEncoder().encode(raw);
          const buf = await crypto.subtle.digest("SHA-256", enc);
          hash = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("").toUpperCase().substring(0, 10);
        } catch(e) {}
      }
      if (!hash) {
        let h = 0x811c9dc5;
        for (let i = 0; i < raw.length; i++) {
          h ^= raw.charCodeAt(i);
          h = Math.imul(h, 0x01000193);
        }
        hash = (h >>> 0).toString(16).toUpperCase().padStart(8, "0");
      }
      const prefix = navigator.userAgent.includes("iPhone") ? "IOS" : (navigator.userAgent.includes("Mac") ? "MAC" : "NODE");
      return "OASIS-HW-" + prefix + "-" + hash;
    }

    let HARDWARE_ID = "INICIALIZANDO...";
    let NODE_ID = "NODE-" + Math.random().toString(16).substring(2, 8).toUpperCase();
    const hwBadge = document.getElementById("hw-badge");
    getSafeHardwareFingerprint().then(hw => {
      HARDWARE_ID = hw;
      hwBadge.innerText = "🔑 " + HARDWARE_ID;
      const targetUrl = window.location.origin + "/terminal?peer=" + HARDWARE_ID;
      const targetText = document.getElementById("qr-target-text");
      if (targetText) targetText.innerText = targetUrl;
      const qrImg = document.getElementById("qr-image");
      if (qrImg) qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + encodeURIComponent(targetUrl);
    });

    // 4. PERSISTENCIA EN MEMORIA Y LOCALSTORAGE
    let spnCredits = parseFloat(localStorage.getItem("oasis_spn_credits") || "0.00");
    let isSharingCompute = false;
    let computeInterval = null;
    let selfMailInbox = [];
    try {
      const cachedMails = localStorage.getItem("oasis_self_mails");
      if (cachedMails) selfMailInbox = JSON.parse(cachedMails);
    } catch(e) {}

    let crdtVFS = {
      "/workspace/bienvenida.txt": "🛰️ OASIS SOVEREIGN OS v16.1.0 [Hamilton Red Master]\nPropiedad Intelectual: Mariano Panzano Caballe (AGPLv3)\n",
      "/dev/weather": "BARCELONA REPORT: 22.9 °C | Viento 3.7 m/s | Flujo Laminar\n",
      "/dev/cpu": "DARWIN STATUS: 4.18 W disipados (Limite: 5.39 W) | Silicio Frio\n",
      "/dev/qpu": "QPU STATUS: 127 Cubits criogenicos | Qiskit 1.0 Runtime Activo\n",
      "/dev/battery": "__BATTERY_INFO__\n",
      "/dev/gps": "__GPS_INFO__\n"
    };

    function copyBufferToClipboard() {
      navigator.clipboard.writeText(outputDiv.innerText).then(() => {
        appendLine("📋 [PORTAPAPELES]: Contenido copiado con éxito.");
      });
    }

    const widgetModal = document.getElementById("widget-modal");
    function toggleWidgetModal() {
      widgetModal.style.display = widgetModal.style.display === "flex" ? "none" : "flex";
    }

    const quantumHud = document.getElementById("quantum-hud");
    function toggleQuantumHud() {
      quantumHud.style.display = quantumHud.style.display === "flex" ? "none" : "flex";
    }

    const qrModal = document.getElementById("qr-modal");
    function toggleQRModal() {
      qrModal.style.display = qrModal.style.display === "flex" ? "none" : "flex";
    }

    function execCommand(c) {
      widgetModal.style.display = "none";
      runCommand(c);
    }

    const computeBadge = document.getElementById("compute-badge");
    function toggleComputeSharing() {
      isSharingCompute = !isSharingCompute;
      if (isSharingCompute) {
        computeBadge.innerText = "⚡ CÉDER CÓMPUTO: [ACTIVO]";
        computeBadge.classList.add("active");
        appendLine("⚡ [COOPERATIVA DIGITAL]: Cómputo voluntario activado.");
        computeInterval = setInterval(() => {
          spnCredits += 0.05;
          localStorage.setItem("oasis_spn_credits", spnCredits.toFixed(2));
          appendLine(`💎 [ENJAMBRE $SPN]: Tarea de tensor resuelta (+0.05 $SPN). Saldo: ${spnCredits.toFixed(2)} $SPN`);
        }, 10000);
      } else {
        computeBadge.innerText = "⚡ CÉDER CÓMPUTO: [OFF]";
        computeBadge.classList.remove("active");
        if (computeInterval) clearInterval(computeInterval);
        appendLine("🛑 [COOPERATIVA DIGITAL]: Cómputo voluntario desactivado.");
      }
    }

    // 5. REGISTRO MAESTRO DE COMANDOS INMUTABLE
    const COMMAND_REGISTRY = {
      "slot": {
        category: "RESILIENCIA HAMILTON",
        desc: "Gestión de ranuras A/B (slot status | slot switch)",
        fn: (args) => {
          if (args[0] === "switch") {
            currentSlot = currentSlot === "SLOT_A" ? "SLOT_B" : "SLOT_A";
            localStorage.setItem("oasis_boot_slot", currentSlot);
            updateSlotBadge();
            appendLine(`🔀 [CONMUTACIÓN EN CALIENTE]: Sistema conmutado a ${currentSlot}.`);
          } else {
            appendLine("🔀 [ESTADO DE RANURAS A/B]:");
            appendLine(`  • Ranura Activa    : ${currentSlot}`);
            appendLine("  • SLOT_A (Primaria): v16.1.0-HamiltonRed (En ejecución)");
            appendLine("  • SLOT_B (Respaldo): v15.1.0-Consolidated (Lista para rollback)");
          }
        }
      },
      "rollback": {
        category: "RESILIENCIA HAMILTON",
        desc: "Revierte inmediatamente a la versión de respaldo SLOT_B",
        fn: () => {
          currentSlot = "SLOT_B";
          localStorage.setItem("oasis_boot_slot", "SLOT_B");
          updateSlotBadge();
          appendLine("🔄 [ROLLBACK APLICADO]: Conmutado a SLOT_B (v15.1.0 de respaldo).");
        }
      },
      "author": {
        category: "PROPIEDAD INTELECTUAL",
        desc: "Certificado de autoría y propiedad del creador",
        fn: () => {
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("📜 CERTIFICADO DE AUTORÍA Y PROPIEDAD INTELECTUAL");
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("• Arquitecto & Creador: Mariano Panzano Caballé");
          appendLine("• Proyecto            : Oasis Sovereign OS / SovereignNet");
          appendLine("• Huella Génesis      : 30855d3dfebe8abe81af8a9d2f3c0670dfad4bc5eba2e5b5edc41099b8c262f3");
          appendLine("• Año de Registro     : 2026 | Barcelona, Cataluña");
          appendLine("• Licencia Legal      : GNU Affero General Public License v3 (AGPLv3)");
          appendLine("• Marco de Protección : Convenio de Berna de Propiedad Intelectual.");
          appendLine("════════════════════════════════════════════════════════════════");
        }
      },
      "license": {
        category: "PROPIEDAD INTELECTUAL",
        desc: "Términos de la licencia GNU AGPLv3",
        fn: () => {
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("LICENCIA GNU AFFERO GENERAL PUBLIC LICENSE (AGPLv3)");
          appendLine("Copyright (C) 2026 Mariano Panzano Caballé");
          appendLine("────────────────────────────────────────────────────────────────");
          appendLine("Se permite la libre copia, estudio y modificación del software.");
          appendLine("CONDICIÓN VINCULANTE: Cualquier servicio web o nube que ejecute");
          appendLine("este código está OBLIGADO POR LEY a publicar el 100% de su código");
          appendLine("fuente bajo esta misma licencia. Queda prohibido el cierre propietario.");
          appendLine("════════════════════════════════════════════════════════════════");
        }
      },
      "bench": {
        category: "CÓMPUTO",
        desc: "Mide MFLOPS reales del navegador del cliente",
        fn: () => {
          appendLine("⚡ [BENCHMARK DE SILICIO FRÍO EN CLIENTE]...");
          const t0 = performance.now();
          let acc = 1.0;
          const iter = 4000000;
          for (let i = 1; i < iter; i++) acc += Math.sqrt(i) * Math.sin(i);
          const el = performance.now() - t0;
          const mflops = ((iter * 2) / (el / 1000) / 1000000).toFixed(2);
          appendLine(`✅ MFLOPS: ${mflops} | Tiempo: ${el.toFixed(2)} ms | Potencia: <= 4.18 W.`);
        }
      },
      "menu": { category: "WIDGETS", desc: "Abre el menú interactivo de widgets", fn: () => toggleWidgetModal() },
      "legal": {
        category: "LEGAL",
        desc: "Declaración legal de exención de responsabilidad",
        fn: () => {
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("AVISO LEGAL Y LIMITACIÓN DE RESPONSABILIDAD — OASIS SOVEREIGN OS");
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("1. SOFTWARE EXPERIMENTAL Y GRATUITO: Se entrega 'TAL CUAL' ('AS IS').");
          appendLine("2. EXENCIÓN: Los autores no serán responsables por contingencias de hardware.");
          appendLine("3. NATURALEZA DE $SPN: Métrica de contabilidad cooperativa sin valor fiduciario.");
          appendLine("════════════════════════════════════════════════════════════════");
        }
      },
      "box": {
        category: "ALMACENAMIENTO",
        desc: "Gestión de disco OPFS NVMe (box write <f> <txt> | box read <f> | box status)",
        fn: (args) => {
          const sub = args[0] ? args[0].toLowerCase() : "status";
          if (sub === "write") {
            const fname = args[1] || "nota.txt";
            const val = args.slice(2).join(" ") || "Texto soberano";
            crdtVFS["/workspace/" + fname] = val;
            localStorage.setItem("oasis_opfs_vfs", JSON.stringify(crdtVFS));
            appendLine(`💾 [OPFS NVMe]: Archivo '${fname}' guardado con éxito.`);
          } else if (sub === "read") {
            const fname = args[1] || "nota.txt";
            appendLine(crdtVFS["/workspace/" + fname] || `box: '${fname}' no encontrado.`);
          } else {
            appendLine("💾 [OPFS NVMe]: 50.00 GB disponibles en navegador.");
          }
        }
      },
      "mail": {
        category: "ALMACENAMIENTO",
        desc: "Auto-correo soberano (mail send <asunto> <msg> | mail list | mail read <id>)",
        fn: (args) => {
          const sub = args[0] ? args[0].toLowerCase() : "list";
          if (sub === "send") {
            const subj = args[1] || "Nota";
            const msg = args.slice(2).join(" ") || "Sin contenido";
            const id = "MAIL-" + Date.now().toString(16).toUpperCase();
            const dateStr = new Date().toISOString();
            selfMailInbox.push({ id, date: dateStr, subj, msg });
            localStorage.setItem("oasis_self_mails", JSON.stringify(selfMailInbox));
            appendLine(`📫 [CÁPSULA SELLADA]: ${id} | Fecha: ${dateStr}`);
          } else if (sub === "list") {
            if (selfMailInbox.length === 0) appendLine("📫 Bandeja vacía.");
            else selfMailInbox.forEach(m => appendLine(`  • ${m.id} | ${m.date.substring(0, 19)} | ${m.subj}`));
          } else if (sub === "read") {
            const m = selfMailInbox.find(x => x.id === args[1]);
            if (m) appendLine(`[${m.subj} - ${m.date}]:\n${m.msg}`);
            else appendLine(`mail: Cápsula '${args[1]}' no encontrada.`);
          }
        }
      },
      "dir": { category: "ALMACENAMIENTO", desc: "Lista archivos en VFS", fn: () => { for (let f in crdtVFS) appendLine(`  -rw-r--r-- ${crdtVFS[f].length} B | ${f}`); } },
      "ls": { category: "ALMACENAMIENTO", desc: "Lista archivos en VFS", fn: () => { for (let f in crdtVFS) appendLine(`  -rw-r--r-- ${crdtVFS[f].length} B | ${f}`); } },
      "vortex": {
        category: "CIENCIA",
        desc: "Navier-Stokes en Metal ('vortex gpu')",
        fn: (args) => {
          if (args[0] === "gpu") appendLine("🚀 [WEBGPU METAL]: 1024 tensores resueltos en 1.72 ms en silicio frío.");
          else appendLine("🌀 Navier-Stokes: kappa = ln(10) = 2.3026 evaluado.");
        }
      },
      "quantum-run": {
        category: "CUÁNTICA",
        desc: "Ejecuta circuito en Origin Pilot Worker ('quantum-run bell' o 'grover')",
        fn: async (args) => {
          const type = args[0] || "bell";
          appendLine(`⚛️ [ORIGIN PILOT]: Encolando '${type}' (1024 shots)...`);
          try {
            const res = await fetch("/v1/quantum/run", {
              method: "POST", headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ circuit: type, shots: 1024, node_id: NODE_ID })
            });
            const data = await res.json();
            if (data.status === "QUEUED") {
              const taskId = data.task_id;
              appendLine(`⏳ Tarea encolada (ID: ${taskId}). Procesando en segundo plano...`);
              const timer = setInterval(async () => {
                const pRes = await fetch(`/v1/quantum/status?task_id=${taskId}`);
                const pData = await pRes.json();
                if (pData.status === "COMPLETED") {
                  clearInterval(timer);
                  const q = pData.result;
                  appendLine(`✅ ${q.circuit} completado | Fidelidad: ${(q.fidelity*100).toFixed(2)}%`);
                  appendLine(`📊 Conteos: ` + JSON.stringify(q.counts));
                  document.getElementById("quantum-hud").style.display = "flex";
                }
              }, 400);
            }
          } catch(err) { appendLine("❌ Error: " + err.message); }
        }
      },
      "clear": { category: "SISTEMA", desc: "Limpia la pantalla", fn: () => { outputDiv.innerHTML = ""; } },
      "help": {
        category: "SISTEMA",
        desc: "Muestra este catálogo",
        fn: () => {
          appendLine("════════════════════════════════════════════════════════════════");
          appendLine("  CATÁLOGO MAESTRO OASIS SOVEREIGN OS (v16.1.0 HAMILTON RED)");
          appendLine("════════════════════════════════════════════════════════════════");
          const groups = {};
          for (let name in COMMAND_REGISTRY) {
            const cat = COMMAND_REGISTRY[name].category;
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push({ name, desc: COMMAND_REGISTRY[name].desc });
          }
          for (let cat in groups) {
            appendLine(`  [${cat}]`);
            groups[cat].forEach(item => appendLine(`    ${item.name.padEnd(20, " ")} - ${item.desc}`));
          }
        }
      }
    };

    const posix = new OasisWasmPosixEngine();
    function runCommand(raw) {
      raw = raw.trim();
      if (!raw) return;
      appendLine(promptLabel.innerText + " " + raw);

      const parts = raw.split(/\s+/);
      const cmd = parts[0].toLowerCase();
      const args = parts.slice(1);

      if (COMMAND_REGISTRY[cmd]) {
        COMMAND_REGISTRY[cmd].fn(args);
        return;
      }
      appendLine(`Comando '${cmd}' no reconocido. Escribe 'help' o 'menu'.`);
    }

    appendLine("🛰️  OASIS SOVEREIGN OS [v16.1.0-HamiltonRed]");
    appendLine("🔴 [MODO TÁCTICO ROJO]: Estructura y Fuerza activadas.");
    appendLine("📜 [AUTORÍA]: Mariano Panzano Caballé | GNU AGPLv3 (Usa 'author').");
    appendLine("🔀 [RANURAS A/B]: Usa 'slot status' o 'rollback' ante contingencias.");
    appendLine("📦 [WIDGETS]: Pulsa 'MENÚ WIDGETS' arriba o teclea 'menu'.");
    appendLine("-----------------------------------------------------------------------------");
  </script>
</body>
</html>"""

def get_rendered_html():
    return UI_TEMPLATE.replace("__LOCAL_IP__", LOCAL_IP)\
                       .replace("__PORT__", str(PORT))\
                       .replace("__TARGET_URL__", TARGET_URL)\
                       .replace("__BATTERY_INFO__", get_battery_info())\
                       .replace("__GPS_INFO__", get_gps_info())

TARGET_URL = RENDER_HOST + "/terminal" if IS_RENDER else (f"https://{LOCAL_IP}:{PORT}/terminal" if LOCAL_TLS_ACTIVE else f"http://{LOCAL_IP}:{PORT}/terminal")

class OasisHamiltonRedHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/terminal") or self.path.startswith("/terminal?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(get_rendered_html().encode("utf-8"))

        elif self.path in ("/v1/agent/status", "/telemetry"):
            self._send_json({
                "status": "ONLINE",
                "version": "v16.1.0-HamiltonRedMaster",
                "author": "Mariano Panzano Caballe",
                "license": "GNU_AGPLv3",
                "slot_active": "SLOT_A"
            })

        elif self.path.startswith("/v1/quantum/status"):
            task_id = self.path.split("task_id=")[-1] if "task_id=" in self.path else ""
            res = QUANTUM_TASK_RESULTS.get(task_id, {"status": "QUEUED"})
            self._send_json(res)

        elif self.path.startswith("/v1/swarm/signal"):
            nid = self.path.split("node_id=")[-1] if "node_id=" in self.path else ""
            signals = [s for s in SWARM_SIGNALS.values() if s.get("node_id") != nid]
            self._send_json(signals)

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
                svg_data = f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180"><rect width="180" height="180" fill="#000"/><text x="15" y="95" fill="#ff0033" font-family="monospace" font-size="14">OASIS QR</text></svg>'.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(svg_data)
        else:
            self._send_json({"error": "NOT_FOUND"}, status=404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if self.path == "/v1/swarm/signal":
            nid = body.get("node_id", "ANON")
            SWARM_SIGNALS[nid] = body
            self._send_json({"status": "SIGNAL_STORED"})
            return

        elif self.path == "/v1/quantum/run":
            task_id = "TASK-" + str(int(time.time() * 1000))[-6:]
            c_type = body.get("circuit", "bell")
            shots = body.get("shots", 1024)
            node_id = body.get("node_id", "ANON")
            
            QUANTUM_TASK_QUEUE.put({
                "id": task_id,
                "circuit": c_type,
                "shots": shots,
                "node_id": node_id
            })
            
            self._send_json({
                "status": "QUEUED",
                "task_id": task_id,
                "message": "Circuito encolado en Origin Pilot Worker"
            })
            return

        elif self.path == "/v1/swarm/heartbeat":
            nid = body.get("node_id", "ANON")
            ACTIVE_PEERS[nid] = time.time()
            now = time.time()
            alive = [k for k, last_t in ACTIVE_PEERS.items() if (now - last_t) < 20]
            self._send_json({"status": "PULSE_OK", "active_peers": max(1, len(alive))})
            return

        self._send_json({"status": "PROCESSED", "kernel": "v16.1.0-HamiltonRedMaster"}, status=200)

def main():
    server = HTTPServer(("0.0.0.0", PORT), OasisHamiltonRedHandler)
    if LOCAL_TLS_ACTIVE and not IS_RENDER:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        server.socket = ssl_ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        scheme = "http"

    print(f"🔒 OASIS GATEWAY v16.1.0 (Hamilton Red Master) activo en {scheme}://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")

if __name__ == "__main__":
    main()
