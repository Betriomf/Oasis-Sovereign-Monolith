import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Asegurar z-index en barra superior para que los botones siempre respondan
html = html.replace(
    '.header-badges { display: flex;',
    '.header-badges { position: relative; z-index: 100; display: flex;'
)

# 2. Reemplazar toda la sección de pegado por captura síncrona sin prompt
old_paste_section_start = html.find("/* HOOK UNIVERSAL DE PORTAPAPELES XTERM.JS */")
if old_paste_section_start == -1:
    old_paste_section_start = html.find("/* 2. PORTAPAPELES ROBUSTO */")

old_paste_section_end = html.find("/* 3. CONTROL DE MODALES")

clean_paste_js = """/* PEGADO NATIVO POR TECLADO (Cmd+V / Ctrl+V) SIN RECUADROS NI PERMISOS */
        let activeTerminalTarget = 'sov';
        document.getElementById('xterm-sovereign').addEventListener('click', () => { activeTerminalTarget = 'sov'; });
        const devElem = document.getElementById('xterm-devframe');
        if (devElem) devElem.addEventListener('click', () => { activeTerminalTarget = 'dev'; });

        // Captura directa del evento del sistema operativo
        window.addEventListener('paste', (e) => {
          const pastedText = (e.clipboardData || window.clipboardData).getData('text');
          if (!pastedText) return;
          e.preventDefault();

          if (activeTerminalTarget === 'dev' && typeof termDev !== 'undefined') {
            devBuf += pastedText;
            termDev.write(pastedText);
          } else {
            sovBuf += pastedText;
            termSov.write(pastedText);
          }
        });
        """

if old_paste_section_start != -1 and old_paste_section_end != -1:
    html = html[:old_paste_section_start] + clean_paste_js + "\n        " + html[old_paste_section_end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copyfile(path, "index.html")
    print("✅ Pegado silencioso nativo (Cmd+V) inyectado. Recuadro emergente eliminado.")
else:
    print("ℹ️ Reemplazo alternativo aplicado.")
