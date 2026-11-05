import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Asegurar carga de Monaco Editor en <head>
if "vs/loader.js" not in html:
    html = html.replace("</head>", '  <script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js"></script>\n</head>')

# 2. Corregir contenedor DevFrame derecho para incrustar ttyd nativo
old_dev_pane = html[html.find('<div class="terminal-pane" id="pane-devframe">'):html.find('</div>\n  </div>\n\n  <!-- MODAL')]
new_dev_pane = '''<div class="terminal-pane" id="pane-devframe">
      <div class="pane-title" style="color: #ffd700;">
        <span>💻 DEVFRAME PTY SHELL (ttyd / C-libuv)</span>
        <div>
          <button onclick="document.getElementById('ttyd-frame').src='http://127.0.0.1:7681?t='+Date.now()" style="background:transparent; border:1px solid #ffd700; color:#ffd700; font-size:10px; border-radius:3px; padding:2px 6px; cursor:pointer;">🔄 RECONECTAR</button>
          <span style="color: #ffaa44; font-size: 10px; margin-left:6px;">PTY DARWIN</span>
        </div>
      </div>
      <div style="flex:1; width:100%; height:100%; background:#020503; border-radius:4px; overflow:hidden;">
        <iframe id="ttyd-frame" src="http://127.0.0.1:7681" style="width:100%; height:100%; border:none;" onerror="console.warn('ttyd no disponible')"></iframe>
      </div>
    </div>'''

if old_dev_pane:
    html = html.replace(old_dev_pane, new_dev_pane)

# 3. Sustituir modal por el contenedor de Monaco Editor
old_modal = html[html.find('<!-- MODAL VISOR DE CÓDIGO JS -->'):html.find('<script>\n    /* =====================================================================\n       1. CONSOLE BRIDGE')]
new_modal = '''<!-- MODAL MONACO EDITOR (VS CODE WEB CORE) -->
  <div id="code-modal" class="modal">
    <div class="modal-box" style="max-width:1100px; height:85vh; display:flex; flex-direction:column;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div>
          <span style="font-weight:bold; color:#00ffff; font-size:14px;" id="code-filename">📄 VS CODE EDITOR</span>
          <span style="font-size:11px; color:#88aa99; margin-left:12px;">(Edición en RAM con guardado a disco)</span>
        </div>
        <div style="display:flex; gap:10px;">
          <button onclick="saveMonacoFile()" style="background:#00ff9d; color:#040906; border:none; padding:5px 14px; font-weight:bold; border-radius:4px; cursor:pointer;">💾 GUARDAR</button>
          <button onclick="document.getElementById('code-modal').style.display='none'" style="background:transparent; border:none; color:#ff4444; font-weight:bold; font-size:18px; cursor:pointer;">✕</button>
        </div>
      </div>
      <div id="monaco-container" style="flex:1; width:100%; border:1px solid #005a36; border-radius:6px; overflow:hidden;"></div>
    </div>
  </div>\n\n  '''

if old_modal:
    html = html.replace(old_modal, new_modal)

# 4. Inyectar inicialización de Monaco y soporte de guardado
monaco_logic = '''
    /* MONACO EDITOR ENGINE INTEGRATION */
    let monacoInstance = null;
    let activeEditorFile = "";

    if (typeof require !== "undefined") {
      require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }});
    }

    function openMonacoEditor(filename, content) {
      activeEditorFile = filename;
      document.getElementById('code-filename').textContent = "📄 " + filename;
      document.getElementById('code-modal').style.display = 'flex';

      const ext = filename.split('.').pop();
      const langMap = { 'js': 'javascript', 'json': 'json', 'py': 'python', 'html': 'html', 'lean': 'lean', 'md': 'markdown' };
      const mode = langMap[ext] || 'plaintext';

      if (!monacoInstance && typeof require !== "undefined") {
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
      } else if (monacoInstance) {
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

if "openMonacoEditor" not in html:
    html = html.replace("/* EXPORTACIÓN Y DESCARGA DIRECTA", monaco_logic + "\n    /* EXPORTACIÓN Y DESCARGA DIRECTA")

# 5. Actualizar el banner de versión
html = html.replace("v19.8.3-DevFrame-E2EE", "v19.8.6-ttyd-Monaco")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
shutil.copyfile(path, "index.html")
print("✅ Plantillas actualizadas a v19.8.6 con ttyd y Monaco.")
