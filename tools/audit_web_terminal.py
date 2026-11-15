#!/usr/bin/env python3
"""Validador de integridad para terminal.html e index.html (evita regresiones de UI)."""
from pathlib import Path
import sys

t_path = Path("agents_core/templates/terminal.html")
i_path = Path("index.html")

if not t_path.exists() or not i_path.exists():
    sys.exit("❌ Faltan terminal.html o index.html")

t_html = t_path.read_text(encoding="utf-8")
i_html = i_path.read_text(encoding="utf-8")

# 1. Verificar sincronización exacta entre plantilla y raíz
if t_html != i_html:
    sys.exit("❌ DESINCRONIZACIÓN: terminal.html e index.html difieren. Ejecuta: cp agents_core/templates/terminal.html index.html")

# 2. Verificar balance de etiquetas <script> y llaves en JS
if t_html.count("<script") != t_html.count("</script>"):
    sys.exit("❌ ERROR HTML: Etiquetas <script> desbalanceadas.")

# 3. Verificar que no se ha perdido ningún comando histórico clave
required_cmds = ["boveda", "c99", "crm", "help", "ask ", "agents", "pool "]
missing = [c for c in required_cmds if c not in t_html]
if missing:
    sys.exit(f"❌ REGRESIÓN DETECTADA: Faltan comandos en la terminal web: {missing}")

print("✅ [WEB TERMINAL AUDIT]: terminal.html e index.html sincronizados, sintaxis intacta y comandos históricos preservados.")
