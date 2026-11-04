#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — AGENTE CENTINELA RIONA v19.6.5
Rastreo social abierto, noticias en vivo (Zero-Auth RSS), GitHub RAG real y tramas pi-KB.
"""
import os
import re
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

PI_KB_LIMIT = 3141
DEFAULT_REPO = "Betriomf/Oasis-Sovereign-Monolith"
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

def fetch_real_github(filepath: str = "README.md") -> str:
    """Extrae el archivo auténtico de GitHub."""
    url = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/main/{filepath}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Oasis-Riona/19.6"})
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            clean = "\n".join([line for line in content.splitlines() if line.strip()][:30])
            return clean[:PI_KB_LIMIT]
    except Exception as e:
        return f"[Error conectando a GitHub raw ({filepath}): {e}]"

def fetch_live_news_rss(query: str) -> str:
    """Consulta noticias y resultados de última hora (Google News RSS en español, sin auth)."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=es&gl=ES&ceid=ES:es"
    headlines = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Oasis-Riona-Sentinel)"})
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
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

def fetch_social_reddit(query: str) -> str:
    """Rastreo abierto de redes sociales / foros públicos (Reddit JSON)."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search.json?q={encoded_q}&sort=new&limit=4"
    social_posts = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Oasis-Riona-Social/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            children = data.get("data", {}).get("children", [])
            for c in children:
                d = c.get("data", {})
                title = d.get("title")
                subreddit = d.get("subreddit_name_prefixed", "")
                if title:
                    social_posts.append(f"• [{subreddit}] {title}")
        if social_posts:
            return "\n".join(social_posts)
    except Exception:
        pass
    return ""

def riona_process(prompt: str) -> str:
    """Procesador central de Riona con compresión pi-KB."""
    clean_p = re.sub(r'^(🎭\s*)?riona[:\s]*', '', prompt, flags=re.IGNORECASE).strip()
    p_low = clean_p.lower()

    # 1. RAG de GitHub
    if any(k in p_low for k in ["github", "readme", "repo", "verdad_oasis", "repositorio"]):
        target = "VERDAD_OASIS.txt" if "verdad" in p_low else "README.md"
        data = fetch_real_github(target)
        return f"📦 [RIONA — GITHUB RAG: {DEFAULT_REPO}/{target}]:\n{data}"

    # 2. Búsqueda de noticias en vivo y eventos de última hora (deportes, elecciones)
    live_news = fetch_live_news_rss(clean_p)
    if live_news:
        return f"🛰️ [RIONA — TITULARES Y HECHOS EN VIVO]:\n{live_news}"

    # 3. Rastreo social abierto
    social = fetch_social_reddit(clean_p)
    if social:
        return f"🌐 [RIONA — RASTREO SOCIAL ABIERTO]:\n{social}"

    return f"🛰️ [RIONA]: No se encontraron eventos en vivo para '{clean_p}'. Red en estasis laminar."

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "futbol liga española"
    print(riona_process(q))
