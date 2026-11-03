#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ROUTER HÍBRIDO CON RAG CANÓNICO (PILAR 172 / 190)
Canaliza consultas con prioridad absoluta a la Base de Conocimiento de Capa 0.
"""
import json
import urllib.request
import urllib.parse
import subprocess
import os
import re

OLLAMA_URL = "http://127.0.0.1:11434"
PI_KB_LIMIT = 3141
PILARES_FILE = os.path.expanduser("~/Oasis-Sovereign-Monolith/vault/pilares_oasis_kb.json")

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

def match_internal_pillar(query: str):
    """Detecta si la consulta refiere a un Pilar de Oasis y extrae su verdad canónica."""
    p_low = query.lower()
    if not os.path.exists(PILARES_FILE):
        return None

    try:
        with open(PILARES_FILE, "r", encoding="utf-8") as f:
            kb = json.load(f)
    except Exception:
        return None

    # 1. Búsqueda por número de pilar (ej: "pilar 1", "pilar 2", "pilar 193")
    match = re.search(r'pilar\s*(\d+)', p_low)
    if match:
        p_num = match.group(1)
        if p_num in kb:
            return kb[p_num]
        # Casos compuestos
        if p_num in ["66", "190", "198", "225", "375"]:
            for k in ["50", "172", "193", "224", "371"]:
                if p_num in kb.get(k, {}).get("titulo", ""):
                    return kb[k]

    # 2. Búsqueda semántica por conceptos clave de Oasis
    if "landauer" in p_low or "silicio frio" in p_low or "silicio frío" in p_low:
        return kb.get("1")
    if "pacing" in p_low or "jitter" in p_low or "gaming" in p_low:
        return kb.get("2")
    if "golod" in p_low or "shafarevich" in p_low:
        return kb.get("193")
    if "navier" in p_low or "stokes" in p_low or "kakeya" in p_low:
        return kb.get("376")
    if "lorentz" in p_low or "lorenz" in p_low:
        return kb.get("211")
    if "hafnio" in p_low or "valencia" in p_low or "quimico-cuantico" in p_low:
        return kb.get("212")
    if "quarantine" in p_low or "cuarentena" in p_low or "mero conducto" in p_low:
        return kb.get("50")
    if "depin" in p_low or "swarm" in p_low or "chen-panzano" in p_low:
        return kb.get("371")

    return None

def fetch_capa1_oracle(query: str) -> str:
    clean_q = re.sub(r'[^\w\s]', '', query).strip()
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

    # CAPA 0A: Comprobación de Pilares Canónicos de Oasis (Respuesta Inmediata sin Alucinación)
    pillar_data = match_internal_pillar(prompt)
    if pillar_data:
        ans = f"🏛️ [{pillar_data['titulo'].upper()}]:\n{pillar_data['definicion']}"
        return "CAPA_0_STATIC", ans

    # CAPA 0B: Determinista LINCOS
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

    # CAPA 1: Oráculo de Hechos Verificados
    oracle_context = fetch_capa1_oracle(prompt)

    # Estado de Ollama
    ollama_alive = False
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=0.8) as r:
            if r.status == 200:
                ollama_alive = True
    except Exception:
        ollama_alive = False

    if not ollama_alive:
        if oracle_context:
            return "CAPA_1_AUTONOMOUS", f"🌐 [ORÁCULO SOBERANO - CAPA 1]:\n{oracle_context}"
        return "CAPA_1_AUTONOMOUS", f"🤖 [ORÁCULO]: Consulta '{prompt}' procesada. Para inferencia densa fuera de red, arranca Ollama (`ollama serve`)."

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
    test_q = sys.argv[1] if len(sys.argv) > 1 else "que dice el pilar 2"
    t, p = route_query(test_q)
    print(f"Tipo: {t}\nPayload: {p}")
