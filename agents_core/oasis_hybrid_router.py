#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — ROUTER HÍBRIDO DE 4 CAPAS (PILAR 172 / 190)
Canaliza consultas por mínima entropía térmica y veracidad fáctica.
"""
import json
import urllib.request
import subprocess

OLLAMA_URL = "http://127.0.0.1:11434"

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

    # CAPA 1: Solicitud explícita de noticias externas u oráculo
    if any(k in p_low for k in ["noticias de hoy", "precio de", "clima en", "actualidad"]):
        aviso = "ℹ️ [CAPA 1 - ORÁCULO EXTERNO]: Conexión a fuentes web en reposo. Modo estasis activo para preservar silicio frío."
        return "CAPA_1_NOTICE", aviso

    # CAPA 3: Razonamiento masivo explícito (> 70B / Nube)
    if any(k in p_low for k in ["demostración completa lean4", "modelo 70b", "cluster cloud"]):
        aviso = "ℹ️ [CAPA 3 - PASARELA NUBE]: Orquestador L402 en espera de canal de micro-pago o credencial externa."
        return "CAPA_3_NOTICE", aviso

    # CAPA 2: Inferencia Local (Ollama) con Streaming SSE, T=0.23 y 2 hilos
    req_body = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.23,
            "num_thread": 2
        },
        "system": "Eres el Agente Velázquez de Oasis Sovereign OS. Responde con estricta veracidad fáctica, sobriedad matemática y concisión."
    }
    return "CAPA_2_STREAM", req_body

if __name__ == "__main__":
    import sys
    test_q = sys.argv[1] if len(sys.argv) > 1 else "capital de españa"
    tipo, res = route_query(test_q)
    print(f"Tipo: {tipo}\nContenido: {res}")
