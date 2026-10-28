#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS DARWIN SYSTEM FORENSIC AUDITOR
Audita simultáneamente: APIs Locales, Nube Render, Salud de JS/HTML y Ejecución de Comandos.
"""
import urllib.request, urllib.parse, json, os, sys, time, subprocess, re

LOCAL_URL = "http://127.0.0.1:8080"
RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(REPO_ROOT, "agents_core", "templates", "terminal.html")

def test_http(url, timeout=3.0):
    try:
        t0 = time.perf_counter()
        req = urllib.request.Request(url, headers={"User-Agent": "Oasis-Forensic/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ms = round((time.perf_counter() - t0) * 1000, 1)
            data = r.read()
            return True, r.status, ms, len(data)
    except Exception as e:
        return False, str(e), 0, 0

print("═" * 72)
print("🔍 AUDITORÍA FORENSE OASIS DARWIN & NUBE RENDER")
print("═" * 72)

# --- 1. AUDITORÍA ENDPOINTS LOCALES (MAC) ---
print("\n[FASE 1: ENDPOINTS LOCALES (http://127.0.0.1:8080)]")
endpoints = [
    ("/v1/openapi.json", "OpenAPI 3.0 Spec"),
    ("/v1/math/demon", "Demonio Landauer (3.78 W)"),
    ("/v1/med/mesh-geometry", "Geometría 3D Carótida (1440 nodos)"),
    ("/v1/swarm/nodes", "Malla P2P & Nodos Activos"),
    ("/v1/ai/chat?prompt=capital+de+espana", "Agente IA (Prompt General)"),
    ("/terminal", "Interfaz Web Terminal")
]

all_local_ok = True
for ep, desc in endpoints:
    ok, code, ms, sz = test_http(f"{LOCAL_URL}{ep}")
    if ok and code == 200:
        print(f"  ✅ {desc:<34} [HTTP 200] ({ms:>5.1f} ms, {sz} B)")
    else:
        all_local_ok = False
        print(f"  ❌ {desc:<34} [FALLO: {code}]")

# --- 2. AUDITORÍA NUBE RENDER ---
print("\n[FASE 2: NUBE REMOTA (Render Cloud Edge)]")
ok_r, code_r, ms_r, sz_r = test_http(f"{RENDER_URL}/health", timeout=5.0)
if ok_r:
    print(f"  ✅ Render Gateway Health          [HTTP 200] ({ms_r} ms)")
else:
    print(f"  ⚠️  Render Gateway No Responde     [{code_r}] -> Probable cold-start de Render.")

# --- 3. AUDITORÍA ESTÁTICA DE JAVASCRIPT EN TERMINAL.HTML ---
print("\n[FASE 3: INTEGRIDAD DEL FRONTEND EN TERMINAL.HTML]")
if os.path.exists(HTML_PATH):
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Comprobaciones sintácticas clave
    scripts = re.findall(r"<script[\s\S]*?</script>", html)
    has_three = "three.min.js" in html
    has_pdf = "pdf.min.js" in html
    open_brackets = html.count("{")
    close_brackets = html.count("}")
    
    print(f"  • Bloques <script> detectados     : {len(scripts)}")
    print(f"  • CDN Three.js 3D presente        : {'✅ SÍ' if has_three else '❌ NO'}")
    print(f"  • CDN PDF.js presente             : {'✅ SÍ' if has_pdf else '❌ NO'}")
    print(f"  • Balance de llaves CSS/JS        : {open_brackets} abiertas vs {close_brackets} cerradas")
    
    # Comprobar sintaxis con el compilador nativo de macOS sin ejecutar código
    tmp_js = os.path.join(REPO_ROOT, "vault", "temp_audit.js")
    with open(tmp_js, "w", encoding="utf-8") as f:
        f.write(js_raw)

    osa_cmd = f'''osascript -l JavaScript -e "function run() { try { new Function($.NSString.stringWithContentsOfFileEncodingError('{tmp_js}', $.NSUTF8StringEncoding, null).js); return 'OK'; } catch(e) { return e.toString(); } }"'''
    osa_res = subprocess.run(osa_cmd, shell=True, capture_output=True, text=True)
    out_osa = osa_res.stdout.strip()

    if "OK" in out_osa:
        print("  ✅ Sintaxis JavaScript cliente    : CERO ERRORES (JavaScriptCore check OK)")
    else:
        print(f"  🚨 ERROR SINTAXIS JAVASCRIPT      : {out_osa}")
    if os.path.exists(tmp_js): os.remove(tmp_js)

# --- 4. AUDITORÍA DEL PUENTE DARWIN (/v1/darwin/exec) ---
print("\n[FASE 4: PUENTE DE EJECUCIÓN DARWIN CLI]")
test_cmd = "cat AUTHORS.md"
post_data = json.dumps({"command": test_cmd}).encode("utf-8")
req = urllib.request.Request(f"{LOCAL_URL}/v1/darwin/exec", data=post_data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=3.0) as r:
        res = json.loads(r.read().decode("utf-8"))
        out = res.get("output", "").strip().split("\n")[0]
        print(f"  ✅ Ejecución remota de '{test_cmd}': \"{out[:45]}...\" [Código: {res.get('code')}]")
except Exception as e:
    print(f"  ❌ Fallo en /v1/darwin/exec: {e}")

print("═" * 72)
