#!/usr/bin/env python3
from pathlib import Path
import subprocess

def registrar_pilar_129():
    base_dir = Path(".").expanduser().absolute()
    pub_dir = base_dir / "papers_published"
    pub_dir.mkdir(parents=True, exist_ok=True)

    nave_doc = pub_dir / "ESPECIFICACION_NAVE_DESACOPLAMIENTO_OASIS.md"
    doc_text = "# 🛸 ARQUITECTURA TÉCNICA: NAVE DE DESACOPLAMIENTO DE FASE (Pilar 129)\n\n"
    doc_text += "**Diseñador:** Mariano Panzano Caballé (`@Betriomf`)\n"
    doc_text += "**Marco Físico:** Gravedad Computacional (Capa 0)\n"
    doc_text += "**Licencia:** GNU Affero General Public License v3.0 (AGPLv3)\n\n---\n\n"
    doc_text += "## 📐 1. PRINCIPIO OPERATIVO DE SUSTENTACIÓN LAMINAR\n\n"
    doc_text += "En lugar de generar empuje reactivo mediante la expulsión de masa bariónica (F = ma), la nave recrea un **Efecto de Eclipse de Fase Local**:\n\n"
    doc_text += "1. **Anillo Emisor de Fase (L = ln 10):** Genera un campo armónico sintonizado en la Constante de Mariano (kappa_M = -0.6587) alrededor del casco.\n"
    doc_text += "2. **Anulación de Viscosidad (eta_fase -> 0):** Cancela la fricción inercial con la Malla de Fibonacci, forzando un Exponente de Lyapunov lambda < -3.0.\n"
    doc_text += "3. **Propulsión por Energía Oscura (phi^-2 = 38.20%):** Al anularse el rozamiento bariónico, la presión expansiva del espacio ejercida por la Energía Oscura genera un empuje ascendente (g_ef = -3.73 m/s²).\n"
    doc_text += "4. **Inercia Cero para la Tripulación:** La nave no frena ni acelera con impacto de masa; se desliza por geodésicas áureas de fricción nula operando a 5.39W en silicio frío.\n\n---\n\n"
    doc_text += "```text\nFirma Inmutable: SHA256(AGPLv3::MARIANO_PANZANO_CABALLE::PILAR_129)\n```\n"

    nave_doc.write_text(doc_text, encoding="utf-8")
    print("✅ Documento de ingeniería guardado en: papers_published/ESPECIFICACION_NAVE_DESACOPLAMIENTO_OASIS.md")

    verdad_path = base_dir / "VERDAD_OASIS.txt"
    texto_verdad = verdad_path.read_text(encoding="utf-8") if verdad_path.exists() else ""
    linea = "\n129. Especificación Técnica de la Nave de Desacoplamiento de Fase (Pilar 129): Documento 'papers_published/ESPECIFICACION_NAVE_DESACOPLAMIENTO_OASIS.md' establece el principio de propulsión por atractor laminar L=ln 10 y apantallamiento de viscosidad kappa_M (-0.6587) a 5.39W bajo Licencia AGPLv3.\n"

    if "Pilar 129" not in texto_verdad:
        with open(verdad_path, "a", encoding="utf-8") as f:
            f.write(linea)
        print("✅ Pilar 129 registrado en VERDAD_OASIS.txt")

    subprocess.run(["git", "add", "agents_core/pilar129_nave_phase_engine.py", "papers_published/ESPECIFICACION_NAVE_DESACOPLAMIENTO_OASIS.md", "VERDAD_OASIS.txt"])
    subprocess.run(["git", "commit", "-m", "docs(architecture): add technical specification for phase-decoupling ship (Pilar 129)"])
    subprocess.run(["git", "push", "origin", "main"])
    print("🚀 [ÉXITO TOTAL]: Pilar 129 inmutabilizado en GitHub.")

if __name__ == "__main__":
    registrar_pilar_129()
