#!/usr/bin/env python3
"""
OASIS CAPA 0 — VELÁZQUEZ MINKOWSKI ORCHESTRATOR
Combina escaneo óptico en trama π-KB, filtro causal y streaming local optimizado.
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

def escanear_corpus_navier():
    print("🔍 [1. MINKOWSKI CAUSAL SCAN]: Filtrando pilares hidrodinámicos en O(1)...")
    hallazgos = []
    
    # 1. Extraer pilares axiomáticos
    truth_file = os.path.join(MONOLITH_DIR, "VERDAD_OASIS.txt")
    if os.path.exists(truth_file):
        with open(truth_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if any(k in line.lower() for k in ["navier", "enstrof", "bkm", "pilar 201", "pilar 339"]):
                    hallazgos.append(line.strip())

    # 2. Extraer fórmulas clave en docs/
    doc_files = glob.glob(os.path.join(MONOLITH_DIR, "docs/*NAVIER*.md")) + \
                glob.glob(os.path.join(MONOLITH_DIR, "docs/*PILAR_33*.md")) + \
                glob.glob(os.path.join(MONOLITH_DIR, "docs/*PILAR_201*.md"))
    
    formulas = []
    for doc in doc_files:
        with open(doc, "r", encoding="utf-8", errors="ignore") as f:
            math_blocks = re.findall(r"(\$\$.*?\$\$|\\\[.*?\\\])", f.read(), re.DOTALL)
            if math_blocks:
                formulas.append(f"{os.path.basename(doc)}: {' '.join(math_blocks[:2])}")

    cuerpo = "⟨LINCOS::NAVIER_STOKES_AXIOMS⟩\n"
    cuerpo += "PILARES:\n" + "\n".join(hallazgos[:5]) + "\n\n"
    cuerpo += "FORMULAS_BASE:\n" + "\n".join(formulas[:3]) + "\n"
    
    trama_pi = cuerpo[:PI_FRAME_CHARS]
    print(f"📦 [TRAMA π-KB]: {len(trama_pi)} bytes estructurados sin ruido de fase.")
    return trama_pi

def inferencia_streaming_laminar(trama_pi):
    # Selección: qwen2.5:1.5b u oasis-phi3 si está en memoria viva
    # qwen2.5:1.5b responde en < 2 segundos en Darwin sin riesgo de timeout
    modelo = "qwen2.5:1.5b"
    print(f"🧠 [2. RECONCILIACIÓN DETERMINISTA]: Invocando {modelo} vía socket local...")

    prompt = (
        "INSTRUCTION: Responde exclusivamente con deducción matemática en LaTeX estándar. Cero saludos.\n"
        f"AXIOMAS INYECTADOS:\n{trama_pi}\n\n"
        "TAREA:\n"
        "1. Demuestra cómo el Atractor kappa = ln(10) acota la enstrofía en el Criterio BKM (∫ ||ω||_L∞ dt < ∞).\n"
        "2. Formula la cota diádica de Littlewood-Paley en Besov B^0_∞,∞ para el término de estiramiento (ω·∇)u.\n"
        "LaTeX Output:"
    )

    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.05,
            "num_predict": 280,
            "num_thread": 4
        },
        "keep_alive": "15m"
    }

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    print(f"⚡ [3. SILICIO FRÍO ≤ 5.39W]: Transmitiendo tokens en tiempo real:\n" + "="*70)
    try:
        # Timeout extendido a 90s para absorber cualquier swap inicial
        with urllib.request.urlopen(req, timeout=90) as resp:
            for line in resp:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    sys.stdout.write(chunk.get("response", ""))
                    sys.stdout.flush()
                    if chunk.get("done", False):
                        break
        print("\n" + "="*70)
    except Exception as e:
        print(f"\n❌ Error en enlace local: {e}")

if __name__ == "__main__":
    trama = escanear_corpus_navier()
    inferencia_streaming_laminar(trama)
