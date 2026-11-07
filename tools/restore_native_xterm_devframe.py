import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Reemplazar el contenedor derecho por un div nativo de Xterm
old_pane = html[html.find('<div class="terminal-pane" id="pane-devframe">'):html.find('</div>\n  </div>\n\n  <!-- MODAL BÓVEDA')]
new_pane = '''<div class="terminal-pane" id="pane-devframe">
      <div class="pane-title" style="color: #ffd700;">
        <span>💻 DEVFRAME HOST SHELL (XTERM NATIVO)</span>
        <span style="color: #ffaa44; font-size: 10px;">EJECUCIÓN NATIVA (Host / Render)</span>
      </div>
      <div id="xterm-devframe" class="term-box"></div>
    </div>'''

if old_pane:
    html = html.replace(old_pane, new_pane)

# 2. Inyectar inicialización del motor Xterm derecho
dev_js = '''
        /* DEVFRAME NATIVO XTERM CON PUENTE RPC */
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

        let devBuf = "";
        const devHist = [];
        let devIdx = -1;
        const devPrompt = "\\x1b[1;33mhost@darwin:/workspace$ \\x1b[0m";

        function showDevPrompt() { termDev.write(devPrompt + devBuf); }
        termDev.writeln("\\x1b[1;33m💻 DEVFRAME NATIVO XTERM — CONEXIÓN DIRECTA RPC\\x1b[0m");
        termDev.writeln("\\x1b[90mCompatible con Render (Linux) y macOS local (Darwin).\\x1b[0m");
        termDev.writeln("-----------------------------------------------------------------------------");
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
              runDevHostCmd(raw);
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

        async function runDevHostCmd(cmd) {
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
          } catch(err) {
            termDev.writeln("\\x1b[31m❌ Error RPC: " + err + "\\x1b[0m");
          }
          showDevPrompt();
        }
'''

if "runDevHostCmd" not in html:
    html = html.replace("/* 2. PORTAPAPELES ROBUSTO */", dev_js + "\n        /* 2. PORTAPAPELES ROBUSTO */")

# 3. Soporte para pegar en el panel activo
html = html.replace(
    'if (txt) { sovBuf += txt; termSov.write(txt); return; }',
    'if (txt) { if (activeTerm === "dev") { devBuf += txt; termDev.write(txt); } else { sovBuf += txt; termSov.write(txt); } return; }'
)

# 4. Actualizar banner
html = html.replace("v19.8.7-Sovereign-Stack", "v19.8.8-Native-Xterm-Dual")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
shutil.copyfile(path, "index.html")
print("✅ Interfaz unificada con Xterm.js nativo en ambos paneles (v19.8.8).")
