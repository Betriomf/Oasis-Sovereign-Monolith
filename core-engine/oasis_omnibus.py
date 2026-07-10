#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🛡️ OASIS OMNIBUS: BUS DE CONTEXTO LOCAL UNIFICADO (PAPERS + GITHUB + NOTAS)

import os
import subprocess
import json
from pypdf import PdfReader

print("⏱️ Consolidando omni-contexto local de Oasis...")

def extraer_texto_notas():
    # Lee notas y manifiestos del proyecto
    texto_acumulado = ""
    ruta_fuentes = os.path.expanduser("~/Oasis_Historico/Sources")
    if os.path.exists(ruta_fuentes):
        for archivo in os.listdir(ruta_fuentes):
            if archivo.endswith(".md") or archivo.endswith(".txt"):
                with open(os.path.join(ruta_fuentes, archivo), "r", encoding="utf-8") as f:
                    texto_acumulado += f"\n--- NOTA [{archivo}] ---\n" + f.read()
    return texto_acumulado if texto_acumulado else "No se detectaron manifiestos de fuentes en Sources."

def extraer_texto_papers():
    # Extrae las primeras páginas de cada PDF en la carpeta de históricos
    texto_acumulado = ""
    ruta_papers = os.path.expanduser("~/Oasis_Historico/Papers")
    if os.path.exists(ruta_papers):
        for archivo in os.listdir(ruta_papers):
            if archivo.endswith(".pdf"):
                try:
                    reader = PdfReader(os.path.join(ruta_papers, archivo))
                    # Extraer texto de las primeras 3 páginas (aduana de baja entropía)
                    texto_pdf = ""
                    for i in range(min(3, len(reader.pages))):
                        texto_pdf += reader.pages[i].extract_text()
                    texto_acumulado += f"\n--- PAPER RESEARCH [{archivo}] ---\n" + texto_pdf
                except Exception as e:
                    continue
    return texto_acumulado if texto_acumulado else "No se detectaron PDFs indexados en Papers."

def consolidar_todo():
    # Extraer el estado de tu Git
    try:
        git_logs = subprocess.check_output(["git", "log", "-n", "3", "--pretty=format:%s (%h)"]).decode("utf-8")
    except Exception:
        git_logs = "Fuera de repositorio Git activo."

    omni_data = {
        "CONTEXTO_INTERNO": {
            "MANIFESTOS_FUENTES": extraer_texto_notas(),
            "LITERATURA_PAPERS": extraer_texto_papers(),
            "ESTADO_REPOSITORIO": git_logs
        }
    }

    # Guardar en la caché central inmutable
    os.makedirs("core-engine", exist_ok=True)
    with open("core-engine/omni_context.json", "w", encoding="utf-8") as f:
        json.dump(omni_data, f, indent=2, ensure_ascii=False)
    print("💎 OMNI_CONTEXT_CLOSED: Datos empaquetados en core-engine/omni_context.json")

if __name__ == "__main__":
    consolidar_todo()
