#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 01]: RIONA SENTINEL
Archivo 100% autocontenido (cero dependencias externas, portable a cualquier sistema).
Funcionalidad: Noticias RSS en vivo (Google News ES), búsqueda abierta y consulta a GitHub.
"""
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SSL_CTX = ssl._create_unverified_context()
HEADERS = {"User-Agent": "Mozilla/5.0 (OasisSovereignSentinel/20.2)"}

def fetch_live_news_rss(query: str, max_items: int = 5) -> str:
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}&hl=es&gl=ES&ceid=ES:es"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        xml_data = urllib.request.urlopen(req, timeout=8, context=SSL_CTX).read()
        root = ET.fromstring(xml_data)
        items = []
        for item in root.findall(".//item")[:max_items]:
            title = (item.findtext("title") or "").strip()
            pub = (item.findtext("pubDate") or "")[:16].strip()
            if title:
                items.append(f"- {title} ({pub})" if pub else f"- {title}")
        return "\n".join(items)
    except Exception:
        return ""

def fetch_wikipedia_fallback(query: str) -> str:
    q = urllib.parse.quote(query)
    url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&utf8=&format=json&srlimit=3"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        data = json.loads(urllib.request.urlopen(req, timeout=6, context=SSL_CTX).read().decode("utf-8"))
        hits = data.get("query", {}).get("search", [])
        lines = []
        for h in hits:
            snippet = re.sub(r"<[^>]+>", "", h.get("snippet", "")).strip()
            lines.append(f"- {h.get('title')}: {snippet}")
        return "\n".join(lines)
    except Exception:
        return ""

def riona_process(prompt: str) -> str:
    clean_p = re.sub(r"^(?:🎭\s*)?riona[:\s]*", "", prompt, flags=re.IGNORECASE).strip()
    if not clean_p:
        return "🛰️ [RIONA]: Escribe una consulta después de 'riona' (ej: riona barcelona aston villa)."

    news = fetch_live_news_rss(clean_p)
    if news:
        return f"🛰️ [RIONA — TITULARES Y HECHOS EN VIVO]:\n{news}"

    wiki = fetch_wikipedia_fallback(clean_p)
    if wiki:
        return f"🌐 [RIONA — REFERENCIA VERIFICADA]:\n{wiki}"

    return f"🛰️ [RIONA]: Sin eventos recientes para '{clean_p}'. Red en estasis laminar."

if __name__ == "__main__":
    consulta = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "barcelona aston villa"
    print(riona_process(consulta))
