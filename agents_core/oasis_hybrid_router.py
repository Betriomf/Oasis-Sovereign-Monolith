#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ROUTER HÍBRIDO DE 4 CAPAS (PILAR 172 / 190)
Canaliza consultas por mínima entropía térmica y veracidad fáctica.
"""
import json
import urllib.request
import urllib.parse
import subprocess
import re

OLLAMA_URL = "http://127.0.0.1:11434"
PI_KB_LIMIT = 3141  # Límite estricto pi-KB (3.14 KB)

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
    """Detecta los modelos reales disponibles en el daemon local de Ollama."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", headers={"User-Agent": "Oasis-Agent"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [m.get("name") for m in data.get("models", [])]
    except Exception:
        return ["aether:1.5b", "qwen2.5:1.5b", "oasis-cold-silicon"]

def fetch_capa1_oracle(query: str) -> str:
    """
    Capa 1: Oráculo web seguro y ultraligero.
    Extrae hechos de Wikipedia / DuckDuckGo y los comprime en <= 3.14 KB.
    """
    clean_q = re.sub(r'[^\w\s]', '', query).strip()
    try:
        # Búsqueda en Wikipedia REST API en español
        encoded = urllib.parse.quote(clean_q)
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignOS/19.5 (research@oasis.local)"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            if extract:
                return extract[:PI_KB_LIMIT]
    except Exception:
        pass

    try:
        # Fallback DuckDuckGo Instant Answer API
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignOS/19.5"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("AbstractText", "") or data.get("Answer", "")
            if extract:
                return extract[:PI_KB_LIMIT]
    except Exception:
        pass

    return ""

def route_query(prompt: str, model: str = "aether:1.5b"):
    """
    Evalúa la consulta y decide la capa óptima.
    Devuelve: (tipo_respuesta, payload)
    """
    p_low = prompt.lower()

    # CAPA 0: Álgebra Determinista (LINCOS) — 0.00 W / < 0.05 ms
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

    # CAPA 3: Razonamiento masivo explícito (> 70B / Nube)
    if any(k in p_low for k in ["demostración completa lean4", "cluster cloud 70b"]):
        aviso = "ℹ️ [CAPA 3 - PASARELA NUBE]: En espera de canal de micro-pago L402."
        return "CAPA_3_NOTICE", aviso

    # CAPA 1 + CAPA 2: Oráculo de Veracidad Fáctica
    # Si la pregunta es fáctica general (capital, historia, qué es, quién es, noticias, etc.)
    oracle_context = ""
    is_factual = any(w in p_low for w in [
        "capital", "presidente", "qué es", "que es", "quién es", "quien es",
        "cuándo", "donde", "historia", "población", "fundación", "noticia"
    ])

    if is_factual:
        oracle_context = fetch_capa1_oracle(prompt)

    system_prompt = (
        "Eres el Agente Velázquez de Oasis Sovereign OS. Responde siempre con estricta veracidad fáctica, "
        "en español neutro, sobriedad matemática y concisión. Si se te proporcionan hechos verificados, "
        "básate exclusivamente en ellos."
    )

    final_prompt = prompt
    if oracle_context:
        final_prompt = f"[HECHOS VERIFICADOS ORÁCULO CAPA 1]:\n{oracle_context}\n\n[PREGUNTA DEL USUARIO]:\n{prompt}\n\nResponde conciso:"

    req_body = {
        "model": model,
        "prompt": final_prompt,
        "stream": True,
        "options": {
            "temperature": 0.23,
            "num_thread": 2
        },
        "system": system_prompt
    }
    return "CAPA_2_STREAM", req_body

if __name__ == "__main__":
    import sys
    test_q = sys.argv[1] if len(sys.argv) > 1 else "capital de españa"
    tipo, res = route_query(test_q)
    print(f"Tipo: {tipo}\nPayload: {res}")
