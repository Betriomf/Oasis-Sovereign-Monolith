#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — AGENTE CENTINELA RIONA v19.7.5 (CASCADA RESILIENTE)
Rastreo multicanal: GitHub RAG -> Google News RSS -> DuckDuckGo Web -> Wikipedia -> Estasis
"""
import os
import re
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

PI_KB_LIMIT = 3141
DEFAULT_REPO = "Betriomf/Oasis-Sovereign-Monolith"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def fetch_real_github(filepath: str = "README.md") -> str:
    url = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/main/{filepath}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            clean = "\n".join([line for line in content.splitlines() if line.strip()][:25])
            return clean[:PI_KB_LIMIT]
    except Exception as e:
        return f"[Error conectando a GitHub raw: {e}]"

def fetch_live_news_rss(query: str) -> str:
    clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
    encoded_q = urllib.parse.quote(clean_q)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=es&gl=ES&ceid=ES:es"
    headlines = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall(".//item")[:5]:
                title = item.find("title")
                pub_date = item.find("pubDate")
                if title is not None and title.text:
                    t_clean = re.sub(r' - [^-]+$', '', title.text)
                    date_str = pub_date.text[:16] if pub_date is not None and pub_date.text else ""
                    headlines.append(f"• {t_clean} ({date_str})")
        if headlines:
            return "\n".join(headlines)
    except Exception:
        pass
    return ""

def fetch_duckduckgo_open_search(query: str) -> str:
    """Fallback web abierto sin claves si RSS no tiene noticias indexadas."""
    try:
        encoded_q = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_q}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # Extraer snippets de resultados en DuckDuckGo HTML
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            results = []
            for s in snippets[:3]:
                clean_s = re.sub(r'<[^>]+>', '', s).strip()
                if clean_s:
                    results.append(f"• {clean_s}")
            if results:
                return "\n".join(results)
    except Exception:
        pass
    return ""

def riona_process(prompt: str) -> str:
    clean_p = re.sub(r'^(🎭\s*)?riona[:\s]*', '', prompt, flags=re.IGNORECASE).strip()
    p_low = clean_p.lower()

    # 1. RAG de GitHub
    if any(k in p_low for k in ["github", "readme", "repo", "verdad_oasis"]):
        target = "VERDAD_OASIS.txt" if "verdad" in p_low else "README.md"
        data = fetch_real_github(target)
        return f"📦 [RIONA — GITHUB RAG: {DEFAULT_REPO}/{target}]:\n{data}"

    # 2. Canal A: Noticias RSS en vivo
    live_news = fetch_live_news_rss(clean_p)
    if live_news:
        return f"🛰️ [RIONA — TITULARES EN VIVO]:\n{live_news}"

    # 3. Canal B: Fallback de búsqueda web abierta
    web_fallback = fetch_duckduckgo_open_search(clean_p)
    if web_fallback:
        return f"🌐 [RIONA — RESULTADOS WEB ABIERTOS]:\n{web_fallback}"

    return f"🛰️ [RIONA]: Red en estasis laminar. Sin eventos concluyentes para '{clean_p}'."

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "noticias de ciencia"
    print(riona_process(q))
