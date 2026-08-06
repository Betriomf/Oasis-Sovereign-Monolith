#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — GOYA PDF & RELEASE PUBLISHER (Pilar 118)
Agente Goya: Compila 'PAPER_ASIMETRIA_BARIONICA_OASIS.md' a formato HTML/PDF
listo para publicación en Zenodo / viXra y distribución en abierto a 5.39W.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import time
from pathlib import Path

class GoyaPdfExporter:
    def __init__(self, workspace_dir="~/Oasis-Sovereign-Monolith"):
        self.workspace = Path(workspace_dir).expanduser()
        print("🎨📄 [GOYA EXPORTER]: Preparando documento para publicación pública...")

    def exportar_html_imprimible(self) -> str:
        md_file = self.workspace / "PAPER_ASIMETRIA_BARIONICA_OASIS.md"
        html_file = self.workspace / "PAPER_ASIMETRIA_BARIONICA_OASIS.html"

        if not md_file.exists():
            print("⚠️ El paper en Markdown no existe.")
            return ""

        contenido_md = md_file.read_text(encoding="utf-8")
        
        # HTML limpio con MathJax para fórmulas matemáticas bonitas
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resolución de la Asimetría Bariónica — Capa 0</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #222; }}
        h1 {{ color: #003366; border-bottom: 2px solid #003366; padding-bottom: 10px; }}
        h2 {{ color: #005588; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f4f4f4; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 4px; }}
        pre {{ background: #f8f8f8; padding: 15px; border-radius: 6px; overflow-x: auto; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap;">{contenido_md}</pre>
</body>
</html>
"""
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ [HTML EXPORTADO]: Guardado en '{html_file.name}'. Listo para guardar como PDF desde el navegador.")
        return str(html_file)

if __name__ == "__main__":
    exporter = GoyaPdfExporter()
    exporter.exportar_html_imprimible()
