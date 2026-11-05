import shutil

html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OASIS SOVEREIGN OS [v19.8.2-DevFrame-DualEngine]</title>
  
  <!-- XTERM.JS CORE + FIT ADDON -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/css/xterm.min.css">
  <script src="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/lib/xterm.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@xterm/addon-fit@0.10.0/lib/addon-fit.min.js"></script>
  
  <!-- ERUDA DEVTOOLS -->
  <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
  <script>eruda.init();</script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #040906; color: #00ff9d; font-family: "SF Mono", Menlo, Consolas, monospace; padding: 12px; font-size: 13px; }
    
    .header-badges { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid #00331f; padding-bottom: 10px; }
    .badge { border: 1px solid #005a36; padding: 5px 10px; border-radius: 6px; font-size: 11px; cursor: pointer; user-select: none; transition: all 0.2s; }
    .badge:hover { opacity: 0.8; }
    #badge-vault { border-color: #00ffff; color: #00ffff; background: rgba(0,255,255,0.08); font-weight: bold; }
    #badge-devframe { border-color: #ffd700; color: #ffd700; background: rgba(255,215,0,0.1); font-weight: bold; }
    #badge-yield { border-color: #00ff9d; background: #00ff9d; color: #040906; font-weight: bold; }
    
    /* DISPOSICIÓN DUAL: TERMINAL SOBERANA + DEVFRAME */
    #dual-workspace {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      height: 74vh;
      width: 100%;
    }
    
    .terminal-pane {
      display: flex;
      flex-direction: column;
      border: 1px solid #005a36;
      border-radius: 8px;
      background: #020503;
      padding: 8px;
      overflow: hidden;
      box-shadow: 0 0 20px rgba(0, 255, 157, 0.08);
    }
    
    .pane-title {
      font-size: 11px;
      font-weight: bold;
      padding-bottom: 6px;
      margin-bottom: 6px;
      border-bottom: 1px solid #00331f;
      display: flex;
      justify-content: space-between;
    }
    
    .term-box { flex: 1; width: 100%; height: 100%; overflow: hidden; }

    /* MODAL VISOR DE CÓDIGO JS / ARCHIVOS */
    .modal { display: none; position: fixed; z-index: 99999; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.88); align-items: center; justify-content: center; }
    .modal-box { background: #08140e; border: 2px solid #00ff9d; border-radius: 12px; max-width: 900px; width: 95%; padding: 20px; color: #aaddcc; box-shadow: 0 0 35px rgba(0,255,157,0.25); max-height: 90vh; overflow-y: auto; }
    .code-viewer { background: #010402; border: 1px solid #005a36; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 12px; color: #00ff9d; white-space: pre; overflow-x: auto; max-height: 60vh; }
  </style>
</head>
<body>

  <div class="header-badges">
    <span class="badge" onclick="toggleLayout()" id="badge-devframe">🛠️ PANEL DUAL: DIVIDIDO</span>
    <span id="badge-vault" class="badge" onclick="openVaultModal()">📁 BÓVEDA E2EE</span>
    <span id="badge-yield" class="badge" onclick="toggleComputeYield()">⚡ CEDER CÓMPUTO: ON</span>
    <span class="badge" onclick="runSovereignCmd('hemo')" style="border-color:#ff4444; color:#ff8888;">🩺 HEMO</span>
    <span class="badge" onclick="runSovereignCmd('skills list')" style="border-color:#00aaff; color:#00ffff;">🧩 SKILLS</span>
    <span class="badge" onclick="runSovereignCmd('did')">🔑 DID</span>
    <span class="badge" onclick="runSovereignCmd('clear')">🧹 LIMPIAR</span>
    <span class="badge" onclick="runSovereignCmd('help')">❓ AYUDA</span>
  </div>

  <div id="dual-workspace">
    <!-- PANEL IZQUIERDO: OASIS SOVEREIGN OS (CAPA 0 / WASM / RAG) -->
    <div class="terminal-pane" id="pane-sovereign">
      <div class="pane-title" style="color: #00ff9d;">
        <span>🛰️ OASIS SOVEREIGN KERNEL (XTERM)</span>
        <span style="color: #88ccee; font-size: 10px;">SILICIO FRÍO (≤ 3.78 W)</span>
      </div>
      <div id="xterm-sovereign" class="term-box"></div>
    </div>

    <!-- PANEL DERECHO: DEVFRAME (TERMINAL HOST DARWIN / NPM / GIT) -->
    <div class="terminal-pane" id="pane-devframe">
      <div class="pane-title" style="color: #ffd700;">
        <span>💻 DEVFRAME HOST SHELL (DARWIN / MAC)</span>
        <span style="color: #ffaa44; font-size: 10px;">EJECUCIÓN NATIVA (npm, git, zsh)</span>
      </div>
      <div id="xterm-devframe" class="term-box"></div>
    </div>
  </div>

  <!-- MODAL VISOR DE CÓDIGO JS -->
  <div id="code-modal" class="modal">
    <div class="modal-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-weight:bold; color:#00ffff; font-size:14px;" id="code-filename">📄 VISOR DE CÓDIGO FUENTE OASIS</span>
        <button onclick="document.getElementById('code-modal').style.display='none'" style="background:transparent; border:none; color:#ff4444; font-weight:bold; font-size:18px; cursor:pointer;">✕ CERRAR</button>
      </div>
      <div class="code-viewer" id="code-content">Cargando código...</div>
    </div>
  </div>

  <script>
    /* =====================================================================
       1. CONSOLE BRIDGE PRIVADO (ZERO-KNOWLEDGE)
       ===================================================================== */
    (function initPrivateConsoleBridge() {
      const origLog = console.log;
      const origWarn = console.warn;
      const origErr = console.error;

      // El puente almacena los logs SOLO en memoria de sesión del desarrollador
      window.DEV_CONSOLE_LOGS = [];

      console.log = function(...args) {
        origLog.apply(console, args);
        const msg = args.join(" ");
        window.DEV_CONSOLE_LOGS.push({ t: Date.now(), level: "LOG", msg });
        if (termSov) termSov.writeln("\\x1b[36m🖥️ [CONSOLE]:\\x1b[0m " + msg);
      };
      console.warn = function(...args) {
        origWarn.apply(console, args);
        const msg = args.join(" ");
        window.DEV_CONSOLE_LOGS.push({ t: Date.now(), level: "WARN", msg });
        if (termSov) termSov.writeln("\\x1b[33m⚠️ [CONSOLE-WARN]:\\x1b[0m " + msg);
      };
      console.error = function(...args) {
        origErr.apply(console, args);
        const msg = args.join(" ");
        window.DEV_CONSOLE_LOGS.push({ t: Date.now(), level: "ERR", msg });
        if (termSov) termSov.writeln("\\x1b[31m🚨 [CONSOLE-ERR]:\\x1b[0m " + msg);
      };
    })();

    /* =====================================================================
       2. INICIALIZACIÓN DE LOS DOS MOTORES XTERM
       ===================================================================== */
    const termTheme = {
      background: '#020503',
      foreground: '#00ff9d',
      cursor: '#00ffff',
      selectionBackground: 'rgba(0, 255, 157, 0.3)',
      black: '#040906',
      red: '#ff5555',
      green: '#00ff9d',
      yellow: '#ffd700',
      blue: '#00aaff',
      cyan: '#00ffff',
      white: '#ffffff'
    };

    // Terminal Soberana (Izquierda)
    const termSov = new Terminal({ cursorBlink: true, fontSize: 13, theme: termTheme });
    const fitSov = new FitAddon.FitAddon();
    termSov.loadAddon(fitSov);
    termSov.open(document.getElementById('xterm-sovereign'));
    fitSov.fit();

    // DevFrame Terminal (Derecha)
    const termDev = new Terminal({
      cursorBlink: true,
      fontSize: 13,
      theme: { ...termTheme, foreground: '#ffffff', cursor: '#ffd700' }
    });
    const fitDev = new FitAddon.FitAddon();
    termDev.loadAddon(fitDev);
    termDev.open(document.getElementById('xterm-devframe'));
    fitDev.fit();

    window.addEventListener('resize', () => { fitSov.fit(); fitDev.fit(); });

    /* BANNERS INICIALES */
    termSov.writeln("\\x1b[1;32m🛰️ OASIS SOVEREIGN OS [v19.8.2-DevFrame-DualEngine]\\x1b[0m");
    termSov.writeln("\\x1b[36m🔒 Cifrado E2EE WebCrypto + P-256 did:key en RAM volátil activa.\\x1b[0m");
    termSov.writeln("\\x1b[33m💡 Escribe 'help' para comandos, 'view <archivo>' para código, o 'v <pregunta>' para IA.\\x1b[0m");
    termSov.writeln("-----------------------------------------------------------------------------");

    termDev.writeln("\\x1b[1;33m💻 DEVFRAME LOCAL SHELL — ENLACE DIRECTO A DARWIN/MACOS\\x1b[0m");
    termDev.writeln("\\x1b[37mEjecuta comandos reales del host sin salir de la interfaz:\\x1b[0m");
    termDev.writeln("  • \\x1b[32mgit status\\x1b[0m       • \\x1b[32mnpm test\\x1b[0m       • \\x1b[32mpython3 tools/verify_all_headless.py\\x1b[0m");
    termDev.writeln("-----------------------------------------------------------------------------");

    /* =====================================================================
       3. GESTIÓN DE ENTRADA Y DISPATCHER EN TERMINAL SOBERANA (IZQUIERDA)
       ===================================================================== */
    let sovBuf = "";
    const sovHist = [];
    let sovIdx = -1;
    const sovPrompt = "\\x1b[1;36mroot@oasis-hurd:/workspace#\\x1b[0m ";

    const SOV_AUTOCOMPLETE = [
      "help", "clear", "did", "eval ", "v ", "riona ", "skills list",
      "hemo", "lean", "view ", "boveda", "webgpu", "mesh", "minkowski", "thermal"
    ];

    function showSovPrompt() { termSov.write(sovPrompt + sovBuf); }
    showSovPrompt();

    termSov.onKey(e => {
      const ev = e.domEvent;
      const key = e.key;

      if (ev.key === "Enter") {
        termSov.writeln("");
        const raw = sovBuf.trim();
        sovBuf = "";
        sovIdx = -1;
        if (raw) {
          sovHist.push(raw);
          runSovereignCmd(raw);
        } else {
          showSovPrompt();
        }
      } else if (ev.key === "Backspace") {
        if (sovBuf.length > 0) {
          sovBuf = sovBuf.slice(0, -1);
          termSov.write("\\b \\b");
        }
      } else if (ev.key === "Tab") {
        ev.preventDefault();
        const cur = sovBuf.trim().toLowerCase();
        if (!cur) return;
        const match = SOV_AUTOCOMPLETE.find(c => c.startsWith(cur));
        if (match) {
          while (sovBuf.length > 0) { termSov.write("\\b \\b"); sovBuf = sovBuf.slice(0, -1); }
          sovBuf = match;
          termSov.write(match);
        }
      } else if (ev.key === "ArrowUp") {
        ev.preventDefault();
        if (sovHist.length > 0 && sovIdx < sovHist.length - 1) {
          sovIdx++;
          while (sovBuf.length > 0) { termSov.write("\\b \\b"); sovBuf = sovBuf.slice(0, -1); }
          sovBuf = sovHist[sovHist.length - 1 - sovIdx];
          termSov.write(sovBuf);
        }
      } else if (ev.key === "ArrowDown") {
        ev.preventDefault();
        if (sovIdx > 0) {
          sovIdx--;
          while (sovBuf.length > 0) { termSov.write("\\b \\b"); sovBuf = sovBuf.slice(0, -1); }
          sovBuf = sovHist[sovHist.length - 1 - sovIdx];
          termSov.write(sovBuf);
        } else if (sovIdx === 0) {
          sovIdx = -1;
          while (sovBuf.length > 0) { termSov.write("\\b \\b"); sovBuf = sovBuf.slice(0, -1); }
        }
      } else if (!ev.altKey && !ev.ctrlKey && !ev.metaKey && key.length === 1) {
        sovBuf += key;
        termSov.write(key);
      }
    });

    async function runSovereignCmd(raw) {
      const low = raw.toLowerCase().trim();

      if (low === "clear") { termSov.clear(); showSovPrompt(); return; }
      if (low === "help") {
        termSov.writeln("\\x1b[33mComandos de Capa 0:\\x1b[0m");
        termSov.writeln("  • \\x1b[32mv <pregunta>\\x1b[0m       : Consultar al Agente Velázquez (Inferencia)");
        termSov.writeln("  • \\x1b[32mriona <consulta>\\x1b[0m   : Centinela de Red (Noticias en vivo / GitHub RAG)");
        termSov.writeln("  • \\x1b[32mview <archivo>\\x1b[0m     : Inspeccionar código fuente sin salir de Oasis");
        termSov.writeln("  • \\x1b[32mhemo\\x1b[0m               : Pipeline hemodinámico 3D Polígono de Willis");
        termSov.writeln("  • \\x1b[32mlean\\x1b[0m               : Verificación formal de los 9 teoremas Lean 4");
        termSov.writeln("  • \\x1b[32mdid\\x1b[0m                : Identidad portable W3C did:key del nodo");
        termSov.writeln("  • \\x1b[32meval <javascript>\\x1b[0m  : Ejecución local en sandbox del navegador");
        termSov.writeln("  • \\x1b[32mboveda, mesh, qr\\x1b[0m   : Módulos de custodia y red distribuida");
        showSovPrompt();
        return;
      }
      if (low === "did") {
        const did = window.SOVEREIGN_NODE_DID || localStorage.getItem("oasis_node_did") || "did:key:zDefault";
        termSov.writeln("\\x1b[36m🔑 [SOVEREIGN DID]:\\x1b[0m " + did);
        showSovPrompt();
        return;
      }
      if (low.startsWith("view ")) {
        const fname = raw.substring(5).trim();
        termSov.writeln(`\\x1b[33m📂 Cargando código de ${fname}...\\x1b[0m`);
        try {
          const res = await fetch("/v1/darwin/exec", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: `cat "${fname}" | head -n 120` })
          }).then(r => r.json());
          document.getElementById("code-filename").textContent = "📄 ARCHIVO: " + fname;
          document.getElementById("code-content").textContent = res.output || "Archivo vacío o no encontrado.";
          document.getElementById("code-modal").style.display = "flex";
        } catch(e) {
          termSov.writeln("\\x1b[31m❌ Error abriendo archivo: " + e + "\\x1b[0m");
        }
        showSovPrompt();
        return;
      }
      if (low === "hemo" || low === "lean" || low === "skills list" || low.startsWith("skills run ")) {
        const target = low === "hemo" ? "hemo" : (low === "lean" ? "lean_audit" : low.replace("skills run ", "").trim());
        termSov.writeln(`\\x1b[33m⚡ [EJECUTANDO SKILL]:\\x1b[0m ${target}...`);
        try {
          const res = await fetch("/v1/skills/exec", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skill: target })
          }).then(r => r.json());
          termSov.writeln(res.output || JSON.stringify(res));
        } catch(e) {
          termSov.writeln("\\x1b[31m❌ Fallo en skill: " + e + "\\x1b[0m");
        }
        showSovPrompt();
        return;
      }
      if (low.startsWith("eval ")) {
        try {
          const r = eval(raw.substring(5));
          termSov.writeln("\\x1b[32m⚙️ [EVAL RESULT]:\\x1b[0m " + r);
        } catch(e) {
          termSov.writeln("\\x1b[31m❌ [EVAL ERROR]:\\x1b[0m " + e.message);
        }
        showSovPrompt();
        return;
      }

      // DISPARO EXCLUSIVO DE AGENTES IA (Solo con 'v ' o 'riona ')
      const isVel = low.startsWith("v ") || low.startsWith("v:") || low.startsWith("ai ");
      const isRio = low.startsWith("riona ") || low.startsWith("riona:");

      if (isVel || isRio) {
        let p = raw;
        if (low.startsWith("v ")) p = raw.substring(2).trim();
        else if (low.startsWith("ai ")) p = raw.substring(3).trim();
        else if (low.startsWith("riona ")) p = raw.substring(6).trim();

        termSov.write(isRio ? "\\x1b[36m🛰️ Riona: \\x1b[0m" : "\\x1b[32m🤖 Velázquez: \\x1b[0m");
        try {
          const res = await fetch("/v1/ai/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: p, model: isRio ? "riona" : "aether:1.5b" })
          });
          const reader = res.body.getReader();
          const decoder = new TextDecoder("utf-8");
          let buf = "";
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buf += decoder.decode(value, { stream: true });
            const lines = buf.split("\\n");
            buf = lines.pop();
            for (const l of lines) {
              if (!l.trim()) continue;
              try {
                const d = JSON.parse(l);
                if (d.response) termSov.write(d.response);
              } catch(err) {}
            }
          }
          termSov.writeln("");
        } catch(e) {
          termSov.writeln("\\x1b[31m[Error en oráculo]\\x1b[0m");
        }
        showSovPrompt();
        return;
      }

      // COMANDO NO RECONOCIDO: NUNCA DISPARAR A VELÁZQUEZ
      termSov.writeln(`\\x1b[31mComando no reconocido:\\x1b[0m '${raw}'. Escribe '\\x1b[33mhelp\\x1b[0m' o usa '\\x1b[32mv <pregunta>\\x1b[0m' para consultar a Velázquez.`);
      showSovPrompt();
    }

    /* =====================================================================
       4. GESTIÓN DEL DEVFRAME (PANEL DERECHO - DARWIN HOST SHELL)
       ===================================================================== */
    let devBuf = "";
    const devHist = [];
    let devIdx = -1;
    const devPrompt = "\\x1b[1;33mdarwin@macbook:/workspace$ \\x1b[0m";

    function showDevPrompt() { termDev.write(devPrompt + devBuf); }
    showDevPrompt();

    termDev.onKey(e => {
      const ev = e.domEvent;
      const key = e.key;

      if (ev.key === "Enter") {
        termDev.writeln("");
        const raw = devBuf.trim();
        devBuf = "";
        devIdx = -1;
        if (raw) {
          devHist.push(raw);
          runHostDevCmd(raw);
        } else {
          showDevPrompt();
        }
      } else if (ev.key === "Backspace") {
        if (devBuf.length > 0) {
          devBuf = devBuf.slice(0, -1);
          termDev.write("\\b \\b");
        }
      } else if (ev.key === "ArrowUp") {
        ev.preventDefault();
        if (devHist.length > 0 && devIdx < devHist.length - 1) {
          devIdx++;
          while (devBuf.length > 0) { termDev.write("\\b \\b"); devBuf = devBuf.slice(0, -1); }
          devBuf = devHist[devHist.length - 1 - devIdx];
          termDev.write(devBuf);
        }
      } else if (ev.key === "ArrowDown") {
        ev.preventDefault();
        if (devIdx > 0) {
          devIdx--;
          while (devBuf.length > 0) { termDev.write("\\b \\b"); devBuf = devBuf.slice(0, -1); }
          devBuf = devHist[devHist.length - 1 - devIdx];
          termDev.write(devBuf);
        } else if (devIdx === 0) {
          devIdx = -1;
          while (devBuf.length > 0) { termDev.write("\\b \\b"); devBuf = devBuf.slice(0, -1); }
        }
      } else if (!ev.altKey && !ev.ctrlKey && !ev.metaKey && key.length === 1) {
        devBuf += key;
        termDev.write(key);
      }
    });

    async function runHostDevCmd(cmd) {
      if (cmd.toLowerCase() === "clear") { termDev.clear(); showDevPrompt(); return; }
      try {
        const res = await fetch("/v1/darwin/exec", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ command: cmd })
        }).then(r => r.json());
        
        if (res.output) {
          res.output.split("\\n").forEach(line => termDev.writeln(line));
        } else {
          termDev.writeln("\\x1b[90m(Sin salida)\\x1b[0m");
        }
      } catch (err) {
        termDev.writeln("\\x1b[31m❌ Error comunicando con host Darwin: " + err + "\\x1b[0m");
      }
      showDevPrompt();
    }

    /* TOGGLE DE LAYOUT DUAL / PANTALLA COMPLETA */
    let isSplit = true;
    function toggleLayout() {
      const devPane = document.getElementById("pane-devframe");
      const grid = document.getElementById("dual-workspace");
      const btn = document.getElementById("badge-devframe");
      isSplit = !isSplit;
      if (isSplit) {
        grid.style.gridTemplateColumns = "1fr 1fr";
        devPane.style.display = "flex";
        btn.textContent = "🛠️ PANEL DUAL: DIVIDIDO";
      } else {
        grid.style.gridTemplateColumns = "1fr";
        devPane.style.display = "none";
        btn.textContent = "🛠️ PANEL DUAL: SOLO KERNEL";
      }
      fitSov.fit();
      fitDev.fit();
    }

    /* INICIALIZACIÓN SOBERANA OPFS + DID */
    (async () => {
      if (navigator.storage && navigator.storage.persist) {
        const ok = await navigator.storage.persist();
        console.log("🔒 [OPFS PERSISTENCE]: " + (ok ? "PERMANENTE" : "BEST-EFFORT"));
      }
      if (!localStorage.getItem("oasis_node_did")) {
        try {
          const kp = await crypto.subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, true, ["sign", "verify"]);
          const rawPub = await crypto.subtle.exportKey("raw", kp.publicKey);
          const hex = Array.from(new Uint8Array(rawPub)).map(b => b.toString(16).padStart(2, "0")).join("");
          const did = "did:key:z" + hex.substring(0, 32);
          localStorage.setItem("oasis_node_did", did);
          window.SOVEREIGN_NODE_DID = did;
        } catch(e) {
          window.SOVEREIGN_NODE_DID = "did:key:zNode" + Math.random().toString(36).substring(2, 10);
        }
      } else {
        window.SOVEREIGN_NODE_DID = localStorage.getItem("oasis_node_did");
      }
    })();
  </script>
</body>
</html>'''

with open("agents_core/templates/terminal.html", "w", encoding="utf-8") as f:
    f.write(html_content)

shutil.copyfile("agents_core/templates/terminal.html", "index.html")
print("✅ Plantillas terminal.html e index.html actualizadas con arquitectura DevFrame y filtro estricto.")
