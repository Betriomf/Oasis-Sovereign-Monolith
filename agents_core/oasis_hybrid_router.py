import riona_agent
#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ROUTER HÍBRIDO ADAPTATIVO (PILAR 172 / 190)
Distingue entre consultas enciclopédicas y deducción científica generativa en LINCOS.
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

def get_installed_models():
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", headers={"User-Agent": "Oasis-Agent"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [m.get("name") for m in data.get("models", [])]
    except Exception:
        return ["aether:1.5b", "qwen2.5:1.5b", "oraculo-web:capa1"]

def match_explicit_pillar(query: str):
    """Solo intercepta si el usuario pide explícitamente consultar un Pilar catalogado."""
    p_low = query.lower()
    
    # Si el usuario pide generar, deducir o inventar, NO es una consulta estática
    generative_tokens = ["genera", "deduce", "deduzcas", "crea", "inventa", "formula", "original", "complementa", "avanza"]
    if any(tok in p_low for tok in generative_tokens):
        return None

    if not os.path.exists(PILARES_FILE):
        return None

    try:
        with open(PILARES_FILE, "r", encoding="utf-8") as f:
            kb = json.load(f)
    except Exception:
        return None

    # Coincidencia explícita: "pilar X", "que dice el pilar X"
    match = re.search(r'pilar\s*(\d+)', p_low)
    if match:
        p_num = match.group(1)
        if p_num in kb:
            return kb[p_num]

    return None

def fetch_capa1_oracle(query: str) -> str:
    # No consultar Wikipedia si es una deducción matemática formal abstracta
    if any(k in query.lower() for k in ["lincos", "kakeya", "landauer(", "kronecker("]):
        return ""

    clean_q = re.sub(r'[^\w\s]', '', query).strip()
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_q)}"
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignOS/19.5"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            if extract:
                return extract[:PI_KB_LIMIT]
    except Exception:
        pass
    return ""

def route_query(prompt: str, model: str = "aether:1.5b"):
    # Intercepción del Agente Riona (Centinela Red, Deportes, Redes & GitHub)
    p_clean = prompt.lower().strip()
    is_riona = (
        model == "riona" or
        p_clean.startswith("riona") or
        "🎭 riona" in p_clean or
        any(k in p_clean for k in ["partido", "aston villa", "elecciones", "clasificacion", "liga española", "noticias de"])
    )

    if is_riona and not any(k in p_clean for k in ["pilar 3", "pilar 1", "pilar 2", "lincos", "kakeya"]):
        facts = riona_agent.riona_process(prompt)
        return "CAPA_1_AUTONOMOUS", facts

    # Intercepción para Agente Riona (Centinela & GitHub RAG)
    if model == "riona" or prompt.lower().startswith("riona "):
        clean_prompt = prompt[6:].strip() if prompt.lower().startswith("riona ") else prompt
        riona_frame = riona_agent.riona_process(clean_prompt)
        return "CAPA_1_AUTONOMOUS", riona_frame
    # 1. Consulta enciclopédica estricta de un pilar
    explicit_pillar = match_explicit_pillar(prompt)
    if explicit_pillar:
        ans = f"🏛️ [{explicit_pillar['titulo'].upper()}]:\n{explicit_pillar['definicion']}"
        return "CAPA_0_STATIC", ans

    # 2. Hechos del Oráculo Web (solo para preguntas factuales comunes)
    oracle_context = fetch_capa1_oracle(prompt)

    # 3. Comprobar si Ollama está disponible
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
        return "CAPA_1_AUTONOMOUS", f"🤖 [ORÁCULO]: Procesando en modo seguro. Inicia Ollama (`ollama serve`) para inferencia densa."

    # 4. Modo Deductivo / Generación Científica en Silicio Frío
    system_prompt = (
        "Eres el Agente Velázquez de Oasis Sovereign OS. Tu rol es la investigación formal en física "
        "informacional, geometría riemanniana y fluidodinámica de Capa 0. Responde con rigor axiomático, "
        "emplea sintaxis LINCOS PL1 cuando se te solicite, mantén sobriedad matemática y opera en silicio frío."
    )

    final_prompt = prompt
    if oracle_context:
        final_prompt = f"[HECHOS VERIFICADOS]:\n{oracle_context}\n\n[PREGUNTA]:\n{prompt}"

    req_body = {
        "model": model,
        "prompt": final_prompt,
        "stream": True,
        "options": {
            "temperature": 0.35,  # Ligero margen para derivación formal sin perder precisión
            "num_thread": 2
        },
        "system": system_prompt
    }
    return "CAPA_2_STREAM", req_body

if __name__ == "__main__":
    import sys
    test_q = sys.argv[1] if len(sys.argv) > 1 else "deduce una formula lincos para navier stokes"
    t, p = route_query(test_q)
    print(f"Tipo: {t}")
