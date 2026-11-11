import shutil

path = "agents_core/templates/terminal.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Inyectar passthrough de comandos UNIX comunes antes del mensaje de error
old_unrecognized = "termSov.writeln(`\\x1b[31mComando no reconocido:\\x1b[0m '${raw}'. Escribe 'help' o usa 'v <pregunta>'.`);"

new_unrecognized = """// Passthrough transparente a shell para comandos UNIX habituales (ls, pwd, cat, ps, etc.)
      const commonUnix = ["ls", "pwd", "cat ", "date", "whoami", "uname", "ps", "top", "git ", "mkdir ", "touch ", "rm "];
      if (commonUnix.some(u => low === u.trim() || low.startsWith(u))) {
        try {
          const res = await fetch("/v1/darwin/exec", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: raw })
          }).then(r => r.json());
          if (res.output) {
            res.output.split("\\n").forEach(l => termSov.writeln(l));
          }
        } catch(e) {
          termSov.writeln("\\x1b[31mError ejecutando shell: " + e + "\\x1b[0m");
        }
        showSovPrompt();
        return;
      }

      termSov.writeln(`\\x1b[31mComando no reconocido:\\x1b[0m '${raw}'. Escribe 'help' o usa 'v <pregunta>'.`);"""

if old_unrecognized in html and "commonUnix" not in html:
    html = html.replace(old_unrecognized, new_unrecognized)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copyfile(path, "index.html")
    print("✅ Passthrough de comandos shell (ls, pwd, etc.) añadido a terminal.html e index.html.")
else:
    print("ℹ️ La plantilla ya incluye soporte de comandos shell.")
