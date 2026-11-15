#!/usr/bin/env python3
"""
OASIS SOVEREIGN SEARCH & CRAWL ORACLE v3.1 (Strict Timeouts & Fail-Safe)
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
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")

def search_vault_rag(query, max_hits=2):
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
            score += 8
        if score > 0:
            idx = next((low.find(t) for t in terms if low.find(t) != -1), 0)
            snippet = " ".join(content[max(0, idx - 60):idx + 260].split())
            scored.append((score, fname, snippet))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"title": f"Bóveda Oasis: {fn}", "url": f"vault://{fn}", "snippet": sn} for _, fn, sn in scored[:max_hits]]

def search_wikipedia_fast(query, max_hits=1):
    q_enc = urllib.parse.quote(query)
    hits = []
    try:
        wiki_url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={q_enc}&format=json&srlimit=1"
        req = urllib.request.Request(wiki_url, headers={"User-Agent": "OasisWiki/3.1"})
        with urllib.request.urlopen(req, timeout=4) as r:
            wdata = json.loads(r.read().decode("utf-8"))
        for item in wdata.get("query", {}).get("search", []):
            clean_snip = html.unescape(re.sub(r'<[^>]+>', '', item.get("snippet", "")))
            title = item.get("title", "")
            hits.append({
                "title": f"Wikipedia (ES): {title}",
                "url": f"https://es.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                "snippet": clean_snip[:240]
            })
    except Exception:
        pass
    return hits[:max_hits]

def run_oracle(query):
    t0 = time.time()
    q = query.strip()

    # 1. Busqueda local inmediata en la Boveda (RAG sin latencia de red)
    vault_hits = search_vault_rag(q, max_hits=2)
    
    # 2. Busqueda web rapida (con timeout estricto de 4s)
    wiki_hits = search_wikipedia_fast(q, max_hits=1)

    sources = vault_hits + wiki_hits
    if not sources:
        sources = [{"title": "Oasis Sovereign Core", "url": "oasis://local", "snippet": f"Consulta procesada localmente para: {q}"}]

    # Fusion estilo Perplexity: Búsqueda Web/Bóveda + Síntesis con oasis-flash:0.5b si está disponible
    bullets = [f"• [{i+1}] {s['snippet']}" for i, s in enumerate(sources)]
    context_txt = " | ".join(s["snippet"] for s in sources)[:550]
    answer = ""
    engine = "Oasis Hybrid RAG (Web + Bóveda)"
    try:
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=0.3)
        ai_req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps({
                "model": "oasis-flash:0.5b",
                "prompt": f"Responde de forma clara y directa a '{q}' usando estas fuentes verificadas:\n{context_txt}",
                "stream": False,
                "keep_alive": "2m",
                "options": {"num_thread": 2, "num_ctx": 512, "num_predict": 110, "repeat_penalty": 1.618}
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(ai_req, timeout=4.5) as r:
            gen = json.loads(r.read().decode("utf-8")).get("response", "").strip()
            if gen:
                answer = gen + "\n\n" + "\n".join(bullets)
                engine = "Oasis Sovereign Causal Synthesis (AGPLv3) + oasis-flash:0.5b"
    except Exception:
        pass
    if not answer:
        answer = "\n".join(bullets)
    elapsed = round(time.time() - t0, 2)

    out = [
        "════════════════════════════════════════════════════════════════",
        f"🔎 [OASIS HYBRID ORACLE — ask] | Motor: {engine} | {elapsed}s",
        "────────────────────────────────────────────────────────────────",
        answer,
        "────────────────────────────────────────────────────────────────",
        "📚 FUENTES VERIFICADAS (Bóveda + Web en tiempo real):"
    ]
    for i, s in enumerate(sources, 1):
        out.append(f"  [{i}] {s['title']} -> {s['url']}")
    out.append("════════════════════════════════════════════════════════════════")
    return "\n".join(out)

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "CRM y Lean 4"
    print(run_oracle(q))


def crawl_url_to_markdown(url, max_chars=1200):
    """Extrae texto limpio en formato Markdown de cualquier URL publica sin Chromium."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OasisSovereignCrawler/3.1"})
        with urllib.request.urlopen(req, timeout=8) as r:
            raw_html = r.read().decode("utf-8", errors="ignore")
        m_title = re.search(r'<title[^>]*>([\s\S]*?)</title>', raw_html, re.IGNORECASE)
        title = html.unescape(re.sub(r'\s+', ' ', m_title.group(1))).strip() if m_title else url
        cleaned = re.sub(r'<(script|style|nav|footer|header|aside|noscript)[^>]*>[\s\S]*?</\1>', ' ', raw_html, flags=re.IGNORECASE)
        cleaned = re.sub(r'<(p|div|br|h[1-3]|li)[^>]*>', '\n', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
        cleaned = html.unescape(cleaned)
        lines = [re.sub(r'[ \t]+', ' ', ln).strip() for ln in cleaned.splitlines() if len(ln.strip()) > 25]
        return title, "\n".join(lines)[:max_chars]
    except Exception as e:
        return url, f"Error extrayendo URL: {e}"
