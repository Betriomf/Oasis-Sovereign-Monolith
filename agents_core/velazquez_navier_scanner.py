#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — VELÁZQUEZ OPTICAL RAG ULTRA-FAST STREAMER
Escaneo óptico de fuentes + Inferencia Streaming por socket HTTP local.
Autor: Mariano Panzano Caballé (@Betriomf) | Licencia: GNU AGPLv3
"""
import os
import re
import sys
import json
import glob
import urllib.request

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
PI_FRAME_CHARS = 3141

class VelazquezNavierScanner:
    def __init__(self):
        print("🎨 [VELÁZQUEZ OPTICAL RAG]: Escaneando corpus de Navier-Stokes...")

    def escanear_fuentes_monolito(self):
        hallazgos = []
        truth_file = os.path.join(MONOLITH_DIR, "VERDAD_OASIS.txt")
        if os.path.exists(truth_file):
            with open(truth_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if any(k in line.lower() for k in ["navier", "enstrof", "bkm", "vortic"]):
                        hallazgos.append(line.strip())

        doc_files = glob.glob(os.path.join(MONOLITH_DIR, "docs/*NAVIER*.md")) + \
                    glob.glob(os.path.join(MONOLITH_DIR, "docs/*PILAR_33*.md")) + \
                    glob.glob(os.path.join(MONOLITH_DIR, "docs/*PILAR_201*.md"))

        contenido_docs = []
        for doc in doc_files:
            with open(doc, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
                bloques_math = re.findall(r"(\$\$.*?\$\$|\\\[.*?\\\])", texto, re.DOTALL)
                resumen = f"Doc: {os.path.basename(doc)} | Fórmulas: {' '.join(bloques_math[:2])}"
                contenido_docs.append(resumen)

        return hallazgos, contenido_docs

    def empaquetar_trama_lincos(self, lineas_pilares, lineas_docs):
        cuerpo = "⟨LINCOS::CORPUS_NAVIER_STOKES⟩\n"
        cuerpo += "PILARES:\n" + "\n".join(lineas_pilares[:5]) + "\n\n"
        cuerpo += "EXTRACTOS:\n" + "\n".join(lineas_docs[:3]) + "\n"
        return cuerpo[:PI_FRAME_CHARS]

    def auditar_streaming_http(self, trama_lincos, modelo="oasis-phi3-laminar:latest"):
        prompt = (
            "INSTRUCTION: Responde exclusivamente con análisis matemático en LaTeX estándar. Cero saludos.\n"
            f"CONTEXTO ÓPTICO VELÁZQUEZ:\n{trama_lincos}\n\n"
            "TAREA:\n"
            "1. Sintetiza cómo el Atractor kappa = ln(10) acota la enstrofía en el Criterio BKM.\n"
            "2. Dictamina si la solución es incondicional universal o regularidad condicional.\n"
            "LaTeX Output:"
        )

        payload = {
            "model": modelo,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.1,
                "num_predict": 250,
                "num_thread": 4
            },
            "keep_alive": "15m"
        }

        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        print(f"⚡ [INFERENCIA STREAMING EN SILICIO FRÍO ({modelo})]:\n" + "="*70)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                for line in resp:
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        token = chunk.get("response", "")
                        sys.stdout.write(token)
                        sys.stdout.flush()
                        if chunk.get("done", False):
                            break
            print("\n" + "="*70)
        except Exception as e:
            print(f"\n❌ Error de conexión con Ollama HTTP: {e}")

if __name__ == "__main__":
    scanner = VelazquezNavierScanner()
    pilares, docs = scanner.escanear_fuentes_monolito()
    print(f" ├─ Pilares detectados : {len(pilares)}")
    print(f" ├─ Documentos leídos  : {len(docs)}")
    trama = scanner.empaquetar_trama_lincos(pilares, docs)
    print(f" └─ Trama Lincos: {len(trama)} bytes (Contenedor π KB OK)")
    
    scanner.auditar_streaming_http(trama, modelo="oasis-phi3-laminar:latest")
