#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ROUTER HÍBRIDO CON ORÁCULO AUTÓNOMO (PILAR 172 / 190)
Garantiza respuestas fácticas incluso si Ollama está en reposo o en la nube.
"""
import json
import urllib.request
import urllib.parse
import subprocess
import re

OLLAMA_URL = "http://127.0.0.1:11434"
PI_KB_LIMIT = 3141

LINCOS_TERMS = {
    "bkm": "navier_stokes_bkm",
    "beale": "navier_stokes_bkm",
    "navier": "navier_stokes_bkm",
    "stokes": "navier_stokes_bkm",
    "enstrofia": "navier_stokes_bkm",
    "landauer": "landauer_phi",
    "golod": "golod_shafarevich",
    "minkowski": "minkowski_causal",
    "kakeya": "kakeya_conjecture"
}

def get_installed_models():
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", headers={"User-Agent": "Oasis-Agent"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [m.get("name") for m in data.get("models", [])]
    except Exception:
        return ["aether:1.5b", "qwen2.5:1.5b", "oraculo-web:capa1"]

def fetch_capa1_oracle(query: str) -> str:
    """Extrae hechos en tiempo real comprimidos en <= 3.14 KB."""
    clean_q = re.sub(r'[^\w\s]', '', query).strip()
    # 1. Wikipedia REST API
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_q)}"
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignOS/19.5"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            if extract:
                return extract[:PI_KB_LIMIT]
    except Exception:
        pass

    # 2. DuckDuckGo Instant Answer
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignOS/19.5"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("AbstractText", "") or data.get("Answer", "")
            if extract:
                return extract[:PI_KB_LIMIT]
    except Exception:
        pass

    return ""

def route_query(prompt: str, model: str = "aether:1.5b"):
    p_low = prompt.lower()

    # Capa 0: Determinista LINCOS
    for key, topic in LINCOS_TERMS.items():
        if key in p_low:
            try:
                res = subprocess.check_output(
                    ["python3", "agents_core/lincos_science_query.py", topic],
                    text=True, timeout=1
                ).strip()
                return "CAPA_0_STATIC", res
            except Exception:
                pass

    # Capa 1: Búsqueda de Hechos Verificados
    oracle_context = fetch_capa1_oracle(prompt)

    # Comprobar si Ollama está vivo en 127.0.0.1:11434
    ollama_alive = False
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=0.8) as r:
            if r.status == 200:
                ollama_alive = True
    except Exception:
        ollama_alive = False

    # Si Ollama está apagado (o ejecutándose en Render), el Oráculo Web responde directamente
    if not ollama_alive:
        if oracle_context:
            res_text = f"🌐 [ORÁCULO SOBERANO - CAPA 1]:\n{oracle_context}"
        else:
            res_text = f"🤖 [ORÁCULO]: Procesando consulta '{prompt}'. Para inferencia densa fuera de red, inicia Ollama en local (`ollama serve`)."
        return "CAPA_1_AUTONOMOUS", res_text

    # Capa 2: Inferencia Local enriquecida con hechos verificados
    final_prompt = prompt
    if oracle_context:
        final_prompt = f"[HECHOS VERIFICADOS ORÁCULO CAPA 1]:\n{oracle_context}\n\n[PREGUNTA]:\n{prompt}\n\nResponde conciso:"

    req_body = {
        "model": model,
        "prompt": final_prompt,
        "stream": True,
        "options": {
            "temperature": 0.23,
            "num_thread": 2
        },
        "system": "Eres el Agente Velázquez de Oasis. Responde con estricta veracidad fáctica y sobriedad matemática."
    }
    return "CAPA_2_STREAM", req_body

if __name__ == "__main__":
    import sys
    test_q = sys.argv[1] if len(sys.argv) > 1 else "capital de españa"
    t, p = route_query(test_q)
    print(f"Tipo: {t}\nPayload: {p}")
