#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — GOYA ANTI-GRAVITY HTML EXPORTER (Pilar 124)
Exporta 'PAPER_ANTIGRAVEDAD_CAPA0_OASIS.md' a un formato HTML navegable con MathJax.
"""

from pathlib import Path

workspace = Path(".").expanduser()
md_file = workspace / "PAPER_ANTIGRAVEDAD_CAPA0_OASIS.md"
html_file = workspace / "PAPER_ANTIGRAVEDAD_CAPA0_OASIS.html"

if md_file.exists():
    content = md_file.read_text(encoding="utf-8")
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Desacoplamiento Gravitatorio y Fase kappa_M — Capa 0</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #111; background: #fafafa; }}
        h1 {{ color: #0a2540; border-bottom: 2px solid #0a2540; padding-bottom: 8px; }}
        h2 {{ color: #20639b; margin-top: 24px; }}
        code {{ background: #eef2f5; padding: 2px 6px; border-radius: 4px; color: #d7263d; }}
        pre {{ background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; overflow-x: auto; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap; font-family: inherit; background: transparent; color: inherit; padding: 0;">{content}</pre>
</body>
</html>
"""
    html_file.write_text(html_content, encoding="utf-8")
    print(f"✅ HTML compilado con éxito: {html_file.name}")
