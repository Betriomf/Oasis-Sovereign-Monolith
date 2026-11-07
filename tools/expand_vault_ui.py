import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Estilos CSS para scrollbar verde neón y lista expandida
old_css_marker = ".viewer-pane {"
new_css = """/* SCROLLBAR FLUIDA Y LISTA EXPANDIDA DE BÓVEDA */
    #vault-files-list {
      max-height: 420px !important;
      overflow-y: auto !important;
      padding-right: 6px;
    }
    #vault-files-list::-webkit-scrollbar, .viewer-pane::-webkit-scrollbar {
      width: 6px;
    }
    #vault-files-list::-webkit-scrollbar-track, .viewer-pane::-webkit-scrollbar-track {
      background: #020503;
      border-radius: 3px;
    }
    #vault-files-list::-webkit-scrollbar-thumb, .viewer-pane::-webkit-scrollbar-thumb {
      background: #005a36;
      border-radius: 3px;
    }
    #vault-files-list::-webkit-scrollbar-thumb:hover {
      background: #00ff9d;
    }
    .modal-box {
      max-height: 94vh !important;
      max-width: 960px !important;
    }
    """ + old_css_marker

html = html.replace(old_css_marker, new_css, 1)

# 2. Contador de archivos dinámico en el encabezado de la lista
old_header = '<div style="font-size:12px; margin-top:8px; font-weight:bold; color:#00ffff;">📂 ARCHIVOS:</div>'
new_header = '<div id="vault-count-header" style="font-size:12px; margin-top:8px; font-weight:bold; color:#00ffff;">📂 ARCHIVOS CIFRADOS EN REPOSO:</div>'
html = html.replace(old_header, new_header)

# 3. Actualizar función renderVaultFileList para mostrar conteo total
old_render = 'function renderVaultFileList() {'
new_render = """function renderVaultFileList() {
      const list = document.getElementById("vault-files-list");
      if (!list) return;
      list.innerHTML = "";
      const files = getSovereignVaultEncrypted();
      const total = Object.keys(files).length;
      const countHeader = document.getElementById("vault-count-header");
      if (countHeader) countHeader.textContent = `📂 ARCHIVOS CIFRADOS (${total}):`;
"""
html = html.replace(old_render, new_render, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
shutil.copyfile(path, "index.html")
print("✅ Interfaz de Bóveda expandida: scrollbar infinita y visor multiactivo.")
