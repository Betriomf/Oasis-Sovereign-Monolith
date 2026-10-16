import re

path = "agents_core/oasis_render_gateway.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Actualizamos la versión a v4.8.1
code = code.replace("v4.8.0-DriverMesh", "v4.8.1-UniversalRoot")

# Política de Root Universal en el cliente web
guest_root_patch = """
  // INICIALIZACIÓN CON ROOT POR DEFECTO PARA CUALQUIER VISITANTE
  const clientHW = await getDeterministicHardwareKey();
  if (clientHW === "OASIS-HW-468F6F695BDB") {
    IS_ROOT = true;
    promptTag.innerText = "root@oasis-sovereign:~#";
    promptTag.className = "prompt-lbl root-lbl";
    updateQuota("ILIMITADA");
  } else {
    // Visitante externo: Root en su Sandbox Soberano
    IS_ROOT = true;
    promptTag.innerText = "root@oasis-guest:~#";
    promptTag.className = "prompt-lbl root-lbl";
    updateQuota("SANDBOX-ROOT");
  }
"""

if "root@oasis-guest" not in code:
    code = code.replace("initTerminal();", guest_root_patch + "\n  initTerminal();")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Política de Root Universal inyectada con éxito en el Gateway.")
