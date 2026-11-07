import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

paste_engine_code = """
        /* HOOK UNIVERSAL DE PORTAPAPELES XTERM.JS */
        function bindTerminalPaste(termInstance, isDev) {
          termInstance.attachCustomKeyEventHandler(async (ev) => {
            if (ev.type === "keydown" && (ev.metaKey || ev.ctrlKey) && (ev.key === "v" || ev.key === "V")) {
              try {
                const clipText = await navigator.clipboard.readText();
                if (clipText) {
                  if (isDev) { devBuf += clipText; termDev.write(clipText); }
                  else { sovBuf += clipText; termSov.write(clipText); }
                  return false;
                }
              } catch (err) {
                // Fallback directo si el navegador bloquea la lectura automática
                const fallback = prompt("Pega tu texto aquí:");
                if (fallback) {
                  if (isDev) { devBuf += fallback; termDev.write(fallback); }
                  else { sovBuf += fallback; termSov.write(fallback); }
                }
                return false;
              }
            }
            return true;
          });
        }

        bindTerminalPaste(termSov, false);
        if (typeof termDev !== "undefined") bindTerminalPaste(termDev, true);
"""

if "bindTerminalPaste" not in html:
    html = html.replace("/* 2. PORTAPAPELES ROBUSTO */", paste_engine_code + "\n        /* 2. PORTAPAPELES ROBUSTO */")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copyfile(path, "index.html")
    print("✅ Motor de pegado universal Xterm inyectado.")
else:
    print("ℹ️ El motor de pegado ya estaba registrado.")
