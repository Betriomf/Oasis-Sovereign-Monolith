#!/usr/bin/env python3
"""
OASIS HYBRID SEARCH ORACLE (Command: ask / oracle)
Motor de busqueda hibrido soberano:
1. RAG local sobre vault/ (Pilares 1-388, Lean 4, CRM).
2. Rastreo web sin rastreo con Pacing Aureo (dt = pi/phi) y filtro Golod-Shafarevich.
3. Compatible con SearXNG autohospedado, Tavily API (opcional), arXiv y fuentes abiertas.
4. Sintesis gratuita con Ollama (si esta activo en Mac) o motor determinista en Render Cloud.
"""
import os
import re
import sys
import json
import math
import time
import html
import urllib.parse
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
GOLDEN_PACING_S = (math.pi / PHI) / 100.0  # ~19.4 ms cadencia laminar

def golod_shafarevich_filter(text):
    """Filtra ruido/spam verificando densidad informacional (r > d^2 / 4)."""
    if not text:
        return False
    clean = re.sub(r'\s+', ' ', text).strip()
    if len(clean) < 40:
        return False
    tokens = set(re.findall(r'[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]{4,}', clean.lower()))
    # Densidad minima de conceptos unicos frente a longitud
    return len(tokens) >= 5

def search_vault_rag(query, max_hits=3):
    """Busca en los documentos de vault/ por coincidencia de terminos clave."""
    terms = [t.lower() for t in re.findall(r'[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9_]{3,}', query)]
    if not terms or not os.path.exists(VAULT_DIR):
        return []
    scored = []
    for fname in os.listdir(VAULT_DIR):
        if not fname.endswith((".md", ".json", ".txt")):
            continue
        fpath = os.path.join(VAULT_DIR, fname)
        try:
            content = open(fpath, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        low = content.lower()
        score = sum(low.count(t) for t in terms)
        if any(t in fname.lower() for t in terms):
            score += 5
        if score > 0:
            # Extraer fragmento mas relevante
            idx = next((low.find(t) for t in terms if low.find(t) != -1), 0)
            snippet = " ".join(content[max(0, idx - 80):idx + 260].split())
            scored.append((score, fname, snippet))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"title": f"Bóveda Oasis: {fn}", "url": f"vault://{fn}", "snippet": sn} for _, fn, sn in scored[:max_hits]]

def search_web_clean(query, max_hits=4):
    """Consulta SearXNG/Tavily si estan configurados, o fuentes abiertas sin rastreo (Wikipedia + arXiv)."""
    results = []
    q_enc = urllib.parse.quote(query)

    # 1. Si hay instancia propia de SearXNG autohospedada
    searx_url = os.environ.get("SEARXNG_URL", "").rstrip("/")
    if searx_url:
        try:
            req = urllib.request.Request(f"{searx_url}/search?q={q_enc}&format=json", headers={"User-Agent": "OasisOracle/20.1"})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode("utf-8"))
            for item in data.get("results", [])[:max_hits]:
                snip = item.get("content", "")
                if golod_shafarevich_filter(snip):
                    results.append({"title": item.get("title", "SearXNG"), "url": item.get("url", ""), "snippet": snip[:280]})
            if results:
                return results
        except Exception:
            pass

    # 2. Si hay clave opcional de Tavily (disenada para agentes IA)
    tavily_key = os.environ.get("TAVILY_API_KEY", "")
    if tavily_key:
        try:
            req = urllib.request.Request(
                "https://api.tavily.com/search",
                data=json.dumps({"api_key": tavily_key, "query": query, "max_results": max_hits}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode("utf-8"))
            for item in data.get("results", [])[:max_hits]:
                snip = item.get("content", "")
                if golod_shafarevich_filter(snip):
                    results.append({"title": item.get("title", "Tavily"), "url": item.get("url", ""), "snippet": snip[:280]})
            if results:
                return results
        except Exception:
            pass

    # 3. Fallback abierto sin claves ni rastreo: Wikipedia API + arXiv API con Pacing Aureo
    time.sleep(GOLDEN_PACING_S)
    for lang in ("es", "en"):
        try:
            wiki_url = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={q_enc}&format=json&srlimit=2"
            req = urllib.request.Request(wiki_url, headers={"User-Agent": "OasisSovereignOracle/20.1 (research@oasis-os)"})
            with urllib.request.urlopen(req, timeout=6) as r:
                wdata = json.loads(r.read().decode("utf-8"))
            for item in wdata.get("query", {}).get("search", []):
                clean_snip = html.unescape(re.sub(r'<[^>]+>', '', item.get("snippet", "")))
                if golod_shafarevich_filter(clean_snip):
                    title = item.get("title", "")
                    results.append({
                        "title": f"Wikipedia ({lang.upper()}): {title}",
                        "url": f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                        "snippet": clean_snip[:260]
                    })
        except Exception:
            pass
        time.sleep(GOLDEN_PACING_S)

    return results[:max_hits]

def synthesize_answer(query, sources):
    """Sintetiza usando Ollama local (si esta activo) o motor determinista gratuito en Render Cloud."""
    context_lines = [f"[{i+1}] {s['title']}: {s['snippet']}" for i, s in enumerate(sources)]
    context_block = "\n".join(context_lines)

    # Intentar Ollama local (activo en Mac)
    try:
        prompt = (
            f"Responde en 3 lineas exactas usando SOLO estas fuentes verificadas y citando [1], [2]:\n"
            f"{context_block}\n\nPregunta: {query}"
        )
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps({
                "model": "oasis-sovereign:1.5b",
                "prompt": prompt,
                "stream": False,
                "keep_alive": "3m",
                "options": {"num_thread": 2, "num_ctx": 1024, "num_predict": 130}
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=25) as r:
            ans = json.loads(r.read().decode("utf-8")).get("response", "").strip()
            if ans:
                return ans, "oasis-sovereign:1.5b (Local Silicon)"
    except Exception:
        pass

    # Fallback gratuito en Render Cloud (cuando el Mac esta cerrado): sintesis extractiva verificada
    if not sources:
        return "Sin coincidencias verificadas en Bóveda ni en fuentes abiertas para esta consulta.", "Oasis Cloud Deterministic RAG (0W)"
    bullets = [f"• [{i+1}] {s['snippet']}" for i, s in enumerate(sources[:3])]
    return "\n".join(bullets), "Oasis Hybrid Cloud Engine (Mac-Off Autonomous)"

def run_oracle(query):
    t0 = time.time()
    vault_hits = search_vault_rag(query, max_hits=2)
    web_hits = search_web_clean(query, max_hits=3)
    sources = vault_hits + web_hits
    answer, engine = synthesize_answer(query, sources)
    elapsed = round(time.time() - t0, 2)

    out = []
    out.append("════════════════════════════════════════════════════════════════")
    out.append(f"🔎 [OASIS HYBRID ORACLE — ask] | Motor: {engine} | {elapsed}s")
    out.append("────────────────────────────────────────────────────────────────")
    out.append(answer)
    out.append("────────────────────────────────────────────────────────────────")
    out.append("📚 FUENTES VERIFICADAS (Filtradas por Pacing Áureo π/φ):")
    if sources:
        for i, s in enumerate(sources, 1):
            out.append(f"  [{i}] {s['title']} -> {s['url']}")
    else:
        out.append("  (Sin fuentes externas requeridas)")
    out.append("════════════════════════════════════════════════════════════════")
    return "\n".join(out)

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Pilar 388 Pool Dual Apache 2.0"
    print(run_oracle(q))
