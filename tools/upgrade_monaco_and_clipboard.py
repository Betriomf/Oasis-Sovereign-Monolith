import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Cargar el cargador oficial de Monaco Editor (VS Code Engine)
monaco_loader = '''  <!-- MONACO EDITOR (VS CODE WEB CORE) -->
  <script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js"></script>
</head>'''
if "monaco-editor" not in html:
    html = html.replace("</head>", monaco_loader)

# 2. Añadir botón PEGAR y GUARDAR en la interfaz
if 'id="btn-paste-clip"' not in html:
    html = html.replace(
        '<span class="badge" onclick="runSovereignCmd(\'did\')">🔑 DID</span>',
        '<span class="badge" id="btn-paste-clip" onclick="pasteClipboardToActiveTerm()" style="border-color:#00ffff; color:#00ffff;">📋 PEGAR</span>\n    <span class="badge" onclick="runSovereignCmd(\'did\')">🔑 DID</span>'
    )

# 3. Sustituir el modal básico por el contenedor de Monaco Editor
old_modal = '''  <!-- MODAL VISOR DE CÓDIGO JS -->
  <div id="code-modal" class="modal">
    <div class="modal-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-weight:bold; color:#00ffff; font-size:14px;" id="code-filename">📄 VISOR DE CÓDIGO FUENTE OASIS</span>
        <button onclick="document.getElementById('code-modal').style.display='none'" style="background:transparent; border:none; color:#ff4444; font-weight:bold; font-size:18px; cursor:pointer;">✕ CERRAR</button>
      </div>
      <div class="code-viewer" id="code-content">Cargando código...</div>
    </div>
  </div>'''

new_modal = '''  <!-- MODAL MONACO EDITOR (VS CODE IN-BROWSER) -->
  <div id="code-modal" class="modal">
    <div class="modal-box" style="max-width:1100px; height:85vh; display:flex; flex-direction:column;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div>
          <span style="font-weight:bold; color:#00ffff; font-size:14px;" id="code-filename">📄 VS CODE EDITOR</span>
          <span style="font-size:11px; color:#88aa99; margin-left:12px;">(Edición en vivo en espacio de usuario)</span>
        </div>
        <div style="display:flex; gap:10px;">
          <button onclick="saveMonacoFile()" style="background:#00ff9d; color:#040906; border:none; padding:5px 14px; font-weight:bold; border-radius:4px; cursor:pointer;">💾 GUARDAR CAMBIOS</button>
          <button onclick="document.getElementById('code-modal').style.display='none'" style="background:transparent; border:none; color:#ff4444; font-weight:bold; font-size:18px; cursor:pointer;">✕</button>
        </div>
      </div>
      <div id="monaco-container" style="flex:1; width:100%; border:1px solid #005a36; border-radius:6px; overflow:hidden;"></div>
    </div>
  </div>'''

if old_modal in html:
    html = html.replace(old_modal, new_modal)

# 4. Lógica de Portapapeles Nativa + Inicialización de Monaco
clipboard_and_monaco_js = '''
    /* MANEJADOR DE PORTAPAPELES ROBUSTO (SIN PERMISSION DENIED) */
    async function pasteClipboardToActiveTerm() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          if (activeTerminal === 'sov') { sovBuf += text; termSov.write(text); }
          else { devBuf += text; termDev.write(text); }
        }
      } catch(e) {
        const manual = prompt("Pega tu texto aquí y pulsa Aceptar:");
        if (manual) {
          if (activeTerminal === 'sov') { sovBuf += manual; termSov.write(manual); }
          else { devBuf += manual; termDev.write(manual); }
        }
      }
    }

    // Intercepción limpia en Xterm evitando bloqueos de seguridad
    function setupXtermPaste(t, getB, setB) {
      t.attachCustomKeyEventHandler((ev) => {
        if (ev.type === 'keydown' && (ev.metaKey || ev.ctrlKey) && (ev.key === 'v' || ev.key === 'V')) {
          // Dejamos que el evento nativo del navegador 'paste' fluya
          return false;
        }
        return true;
      });
    }
    setupXtermPaste(termSov, () => sovBuf, (v) => { sovBuf = v; });
    setupXtermPaste(termDev, () => devBuf, (v) => { devBuf = v; });

    window.addEventListener('paste', (e) => {
      e.preventDefault();
      const clipText = (e.clipboardData || window.clipboardData).getData('text');
      if (!clipText) return;
      if (activeTerminal === 'sov') {
        sovBuf += clipText;
        termSov.write(clipText);
      } else {
        devBuf += clipText;
        termDev.write(clipText);
      }
    });

    /* INICIALIZACIÓN MONACO EDITOR (VS CODE) */
    let monacoInstance = null;
    let activeEditorFile = "";

    require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }});

    function openMonacoEditor(filename, content) {
      activeEditorFile = filename;
      document.getElementById('code-filename').textContent = "📄 " + filename;
      document.getElementById('code-modal').style.display = 'flex';

      const ext = filename.split('.').pop();
      const langMap = { 'js': 'javascript', 'json': 'json', 'py': 'python', 'html': 'html', 'lean': 'lean', 'md': 'markdown' };
      const mode = langMap[ext] || 'plaintext';

      if (!monacoInstance) {
        require(['vs/editor/editor.main'], function() {
          monacoInstance = monaco.editor.create(document.getElementById('monaco-container'), {
            value: content,
            language: mode,
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 13,
            fontFamily: '"SF Mono", Menlo, Consolas, monospace',
            minimap: { enabled: true }
          });
        });
      } else {
        monaco.editor.setModelLanguage(monacoInstance.getModel(), mode);
        monacoInstance.setValue(content);
      }
    }

    async function saveMonacoFile() {
      if (!activeEditorFile || !monacoInstance) return;
      const newCode = monacoInstance.getValue();
      try {
        const res = await fetch("/v1/darwin/exec", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ command: `cat << 'EOF' > "${activeEditorFile}"\\n${newCode}\\nEOF` })
        }).then(r => r.json());
        alert("✅ Archivo guardado correctamente en disco: " + activeEditorFile);
      } catch(e) {
        alert("❌ Error guardando archivo: " + e);
      }
    }
'''

# Modificar comando 'view' para abrir Monaco en lugar del modal plano
old_view_handler = 'document.getElementById("code-modal").style.display = "flex";'
new_view_handler = 'openMonacoEditor(fname, res.output || "");'
html = html.replace(old_view_handler, new_view_handler)

if "pasteClipboardToActiveTerm" not in html:
    html = html.replace("/* EXPORTACIÓN Y DESCARGA DIRECTA", clipboard_and_monaco_js + "\n    /* EXPORTACIÓN Y DESCARGA DIRECTA")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
shutil.copyfile(path, "index.html")
print("✅ Monaco Editor (VS Code) y Portapapeles sin permisos bloqueados instalados.")
