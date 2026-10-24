#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS ASC & ATLAS CODE INTEGRITY AUDITOR
Verifica ausencia de duplicaciones en plantillas, sintaxis y salud de endpoints.
"""
import os, sys, re, json, urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "agents_core", "templates", "terminal.html")

def audit_template_structure():
    print("🔍 [ASC AUDIT]: Analizando estructura de 'terminal.html'...")
    if not os.path.exists(TEMPLATE_PATH):
        print("❌ Error: terminal.html no existe.")
        return False

    with open(TEMPLATE_PATH, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    errors = []
    # 1. Comprobación de fuga de shell heredoc
    if "heredoc>" in content or "127.0.0.1 - - [" in content:
        errors.append("Fuga de logs de terminal detectada dentro del código HTML.")

    # 2. Comprobación de duplicación de etiquetas maestras
    for tag in ["<!DOCTYPE html>", "<html", "</html>", "<body", "</body>"]:
        count = len(re.findall(re.escape(tag), content, re.IGNORECASE))
        if count > 1:
            errors.append(f"Etiqueta duplicada detectada: '{tag}' aparece {count} veces (pantalla doble).")

    # 3. Comprobación de IDs duplicados críticos
    for el_id in ["termContainer", "webgl-canvas-box", "mesh3d-modal", "cmd"]:
        count = len(re.findall(rf'id=["\']{el_id}["\']', content))
        if count > 1:
            errors.append(f"ID DOM duplicado: '#{el_id}' aparece {count} veces.")

    if errors:
        for err in errors:
            print(f"  ❌ {err}")
        return False

    print("  ✅ Estructura HTML limpia: 1 pantalla única, 0 duplicados, 0 fugas de shell.")
    return True

def audit_live_endpoints():
    print("🔬 [ATLAS AUDIT]: Verificando salud de endpoints locales (Puerto 8080)...")
    endpoints = [
        ("/v1/math/demon", "Demonio Maxwell-Landauer"),
        ("/v1/med/besov-cfd", "Hemodinámica Besov 3D"),
        ("/v1/med/mesh-geometry", "Geometría Vascular VMR"),
        ("/v1/swarm/nodes", "Censo Swarm P2P")
    ]
    all_ok = True
    for ep, name in endpoints:
        url = f"http://127.0.0.1:8080{ep}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Atlas-Auditor"})
            with urllib.request.urlopen(req, timeout=1.8) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    print(f"  ✅ {name}: OK ({url})")
                else:
                    print(f"  ❌ {name}: HTTP {resp.status}")
                    all_ok = False
        except Exception as e:
            print(f"  ❌ {name}: Fallo de conexión ({e})")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    t_ok = audit_template_structure()
    if not t_ok:
        sys.exit(1)
    if len(sys.argv) > 1 and sys.argv[1] == "--live":
        e_ok = audit_live_endpoints()
        sys.exit(0 if (t_ok and e_ok) else 1)
    sys.exit(0)
