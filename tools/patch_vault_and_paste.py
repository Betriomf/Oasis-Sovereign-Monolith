import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Añadir botones de Descarga y Apertura en la Bóveda (Tab 1)
old_viewer_btns = '<button onclick="switchVaultTab(2)" style="margin-top:8px; width:100%; background:#005a36; color:#00ff9d; border:none; padding:8px; border-radius:4px; font-weight:bold; cursor:pointer;">💬 PREGUNTAR A LA IA SOBRE ESTE DOCUMENTO ➡️</button>'

new_viewer_btns = '''<div style="display:flex; gap:8px; margin-top:8px;">
              <button onclick="downloadActiveDoc()" style="flex:1; background:#005a36; color:#00ffff; border:1px solid #00aaff; padding:7px; border-radius:4px; font-weight:bold; cursor:pointer;">⬇️ DESCARGAR</button>
              <button onclick="openActiveDocInNewTab()" style="flex:1; background:#005a36; color:#ffd700; border:1px solid #ffaa00; padding:7px; border-radius:4px; font-weight:bold; cursor:pointer;">↗️ ABRIR EN PESTAÑA</button>
            </div>
            <button onclick="switchVaultTab(2)" style="margin-top:8px; width:100%; background:#00ff9d; color:#040906; border:none; padding:8px; border-radius:4px; font-weight:bold; cursor:pointer;">💬 PREGUNTAR A LA IA SOBRE ESTE DOCUMENTO ➡️</button>'''

html = html.replace(old_viewer_btns, new_viewer_btns)

# 2. Inyectar funciones de exportación/descarga en el script
export_functions = '''
    /* EXPORTACIÓN Y DESCARGA DIRECTA DESDE RAM (ZERO-KNOWLEDGE) */
    function downloadActiveDoc() {
      if (!currentDecryptedText) { alert("Selecciona primero un archivo para descifrar."); return; }
      const blob = new Blob([currentDecryptedText], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = currentActiveDocName || "documento_soberano.txt";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    function openActiveDocInNewTab() {
      if (!currentDecryptedText) { alert("Selecciona primero un archivo para descifrar."); return; }
      const blob = new Blob([currentDecryptedText], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    }
'''

# 3. Sustituir el manejador de pegado por el hook directo de Xterm attachCustomKeyEventHandler
old_paste_listener = '''    // SOPORTE UNIVERSAL DE PEGADO (Cmd+V, Ctrl+V, Menú Contextual)
    window.addEventListener('paste', (e) => {
      const text = e.clipboardData ? e.clipboardData.getData('text') : '';
      if (!text) return;
      if (activeTerminal === 'sov') {
        sovBuf += text;
        termSov.write(text);
      } else {
        devBuf += text;
        termDev.write(text);
      }
    });'''

new_paste_engine = '''    /* HOOK NATIVO DE PORTAPAPELES XTERM.JS (Cmd+V / Ctrl+V / ContextMenu) */
    function attachClipboardHandler(termInstance, getTargetBuf, setTargetBuf) {
      termInstance.attachCustomKeyEventHandler(async (arg) => {
        if (arg.type === "keydown" && (arg.metaKey || arg.ctrlKey) && (arg.key === "v" || arg.key === "V")) {
          try {
            const clipText = await navigator.clipboard.readText();
            if (clipText) {
              setTargetBuf(getTargetBuf() + clipText);
              termInstance.write(clipText);
            }
          } catch(err) {
            console.warn("Acceso portapapeles bloqueado. Usa clic derecho o concede permiso:", err);
          }
          return false; // Evita que Xterm intercepte y descarte el pegado
        }
        return true;
      });
    }

    attachClipboardHandler(termSov, () => sovBuf, (v) => { sovBuf = v; });
    attachClipboardHandler(termDev, () => devBuf, (v) => { devBuf = v; });

    // Fallback estándar en caso de menú contextual "Pegar"
    window.addEventListener('paste', (e) => {
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
''' + export_functions

html = html.replace(old_paste_listener, new_paste_engine)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

shutil.copyfile(path, "index.html")
print("✅ Pegado Xterm y botones de descarga/apertura inyectados en plantillas.")
