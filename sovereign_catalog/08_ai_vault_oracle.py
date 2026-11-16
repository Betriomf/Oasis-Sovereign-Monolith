#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 08]: ORÁCULO IA DE BÓVEDA Y PILARES (`ai` / `v` / `pilares`)
Funciona tanto en Darwin como en Render Cloud 24/7 con el Mac cerrado (0 dependencias externas).
"""
import importlib.util
import json
import re
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = BASE_DIR / "vault"
CATALOG_DIR = Path(__file__).resolve().parent

LIVE_KEYWORDS = (
    "barça", "barcelona", "madrid", "liga", "clasificación", "clasificacion",
    "partido", "elecciones", "noticias", "ayer", "hoy", "resultado", "resultados"
)

def search_vault_rag(query: str, max_hits: int = 3) -> list[tuple[str, str]]:
    if not VAULT_DIR.exists():
        return []
    tokens = [t for t in re.findall(r"[a-z0-9áéíóúüñ]{3,}", query.lower()) if t not in {"que", "dice", "como", "para", "por", "con", "los", "las", "del", "una"}]
    if not tokens:
        return []

    scored = []
    for f in VAULT_DIR.iterdir():
        if not f.is_file() or f.suffix.lower() not in {".md", ".txt", ".json"} or f.stat().st_size > 2_000_000:
            continue
        txt = f.read_text(encoding="utf-8", errors="ignore")
        low = txt.lower()
        score = sum(low.count(tok) for tok in tokens)
        if any(tok in f.name.lower() for tok in tokens):
            score += 15
        if score > 0:
            best_snip = ""
            for line in txt.splitlines():
                clean = line.strip()
                if len(clean) > 25 and any(tok in clean.lower() for tok in tokens):
                    best_snip = clean[:480]
                    break
            if not best_snip:
                best_snip = " ".join(txt.split())[:480]
            scored.append((score, f.name, best_snip))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(name, snip) for _, name, snip in scored[:max_hits]]

def query_ollama_grounded(prompt: str, context: str) -> str:
    sys_prompt = (
        "Eres Velázquez, el oráculo científico de Oasis Sovereign OS. "
        "Responde de forma rigurosa y breve usando SOLO el contexto verificado.\n\n"
        f"CONTEXTO:\n{context}\n\nPREGUNTA: {prompt}"
    )
    try:
        payload = json.dumps({
            "model": "oasis-flash:0.5b",
            "prompt": sys_prompt,
            "stream": False,
            "keep_alive": "5m",
            "options": {"num_thread": 2, "num_ctx": 512, "num_predict": 140, "temperature": 0.1}
        }).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=4) as r:
            return json.loads(r.read().decode("utf-8")).get("response", "").strip()
    except Exception:
        return ""

def ai_process(prompt: str = "") -> str:
    q = re.sub(r"^(?:ai|v|velazquez)[:\s]*", "", prompt, flags=re.I).strip().strip('"').strip("'")
    if not q:
        return "🤖 Velázquez: Escribe tu consulta tras 'ai' (ej: ai \"que dice el pilar 377\")."

    # 1. Actualidad/noticias/deportes -> Delegación en Riona (Módulo 01) en tiempo real
    if any(k in q.lower() for k in LIVE_KEYWORDS) and (CATALOG_DIR / "01_riona_sentinel.py").exists():
        spec = importlib.util.spec_from_file_location("riona_live", str(CATALOG_DIR / "01_riona_sentinel.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return "🤖 Velázquez (vía Centinela Riona en vivo):\n" + mod.riona_process(q)

    # 2. Búsqueda RAG determinista en Bóveda (vault/) y Pilares
    hits = search_vault_rag(q)
    if hits:
        ctx = "\n".join(f"[{name}]: {snip}" for name, snip in hits)
        ai_synthesis = query_ollama_grounded(q, ctx)
        header = f"🤖 Velázquez (RAG Bóveda Verificada — {hits[0][0]}):\n"
        if ai_synthesis:
            return f"{header}{ai_synthesis}\n\n📚 Fuente: {hits[0][1]}"
        return f"{header}{hits[0][1]}"

    # 3. Fallback Wikipedia en español para preguntas enciclopédicas generales (funciona 24/7 sin Mac)
    if (CATALOG_DIR / "01_riona_sentinel.py").exists():
        spec = importlib.util.spec_from_file_location("riona_wiki", str(CATALOG_DIR / "01_riona_sentinel.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        wiki = mod.fetch_wikipedia_fallback(q)
        if wiki:
            return f"🤖 Velázquez (Oráculo Enciclopédico 24/7):\n{wiki}"

    return f"🤖 Velázquez: Sin referencias verificadas para '{q}'. Usa `riona <tema>` para rastreo web."

if __name__ == "__main__":
    print(ai_process(" ".join(sys.argv[1:]) or "que dice el pilar 377"))
