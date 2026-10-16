# -*- coding: utf-8 -*-
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")

def _load(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    if not os.path.exists(path):
        return f"<h1>Error 404: Template '{name}' no encontrado</h1>"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def handle_static_get(path: str, kernel_version: str):
    if path in ("/", "/terminal") or path.startswith("/terminal?"):
        content = _load("terminal.html").replace("{{KERNEL_VERSION}}", kernel_version)
        return (200, "text/html", content.encode("utf-8"))
    elif path.startswith("/sheet"):
        return (200, "text/html", _load("sheet.html").encode("utf-8"))
    elif path in ("/oasis_tab", "/extension/oasis_tab.html"):
        return (200, "text/html", _load("telemetry.html").encode("utf-8"))
    elif path in ("/v86_linux", "/linux"):
        return (200, "text/html", _load("v86_linux.html").encode("utf-8"))
    return None
