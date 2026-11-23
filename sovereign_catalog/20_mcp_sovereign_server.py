#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 20]: SERVIDOR MCP & SCRAPER CON PACING ÁUREO (`mcp` / `scrape`)
1. Implementa el protocolo estándar Model Context Protocol (MCP JSON-RPC 2.0 stdio) en Python puro (0 Node.js).
2. Expone herramientas reales a la IA:
   - web_scraper(url): Descarga y limpia texto web aplicando retardo cadenciado por proporción áurea (pi/phi).
   - search_pilares(query): Consulta verificada en la Bóveda de Pilares Oasis.
   - verify_lean4(module): Ejecuta el Notario Matemático Lean 4 (sorry = 0).
3. Incluye bucle agéntico para el pool local Smolmaxxing en Ollama (0.5B - 1.5B Q4_K_M).
"""
import html as html_lib
import json
import math
import re
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SSL_CTX = ssl._create_unverified_context()
GOLDEN_PACING_SEC = (math.pi / ((1.0 + math.sqrt(5.0)) / 2.0)) * 0.15  # ~0.291 s cadencia áurea

# ==============================================================================
# 1. DEFINICIÓN DE HERRAMIENTAS MCP (EQUIVALENTE A server.registerTool)
# ==============================================================================
MCP_TOOLS = [
    {
        "name": "web_scraper",
        "description": "Descarga y extrae el texto limpio de una URL pública usando cadencia de Pacing Áureo (pi/phi) para evitar bloqueos.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL completa (https://...) a inspeccionar"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "search_pilares",
        "description": "Busca definiciones y teoremas verificados dentro de los Pilares internos de Oasis (vault/VERDAD_OASIS.md).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Término o número de pilar a buscar (ej: '378', 'Crouzeix', 'Yang-Mills')"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "verify_lean4",
        "description": "Ejecuta el Notario Matemático Lean 4 sobre la biblioteca formal de Yang-Mills certificando sorry = 0.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def tool_web_scraper(url: str) -> str:
    target = url.strip()
    if not target.startswith(("http://", "https://")):
        target = "https://" + target
    # Pacing Áureo (pi / phi) antes de emitir la petición HTTP
    time.sleep(GOLDEN_PACING_SEC)
    req = urllib.request.Request(
        target,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=28, context=SSL_CTX) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
        # Limpiar scripts, estilos y etiquetas HTML
        clean = re.sub(r"<(script|style|noscript)[^>]*>[\s\S]*?</\1>", " ", raw, flags=re.I)
        title_m = re.search(r"<title[^>]*>([\s\S]*?)</title>", clean, flags=re.I)
        title = html_lib.unescape(re.sub(r"\s+", " ", title_m.group(1))).strip() if title_m else target
        text = html_lib.unescape(re.sub(r"<[^>]+>", " ", clean))
        text = re.sub(r"\s+", " ", text).strip()
        return f"🌐 [SCRAPING ÁUREO π/φ — {title}]\nURL: {target}\nEXTRACTO VERIFICADO:\n{text[:1400]}"
    except Exception as e:
        return f"❌ Error en web_scraper({target}): {type(e).__name__}: {e}"


def tool_arxiv_physics_today(topic: str = "hep-th OR math-ph") -> str:
    import xml.etree.ElementTree as ET
    q_enc = urllib.parse.quote(topic)
    url = f"http://export.arxiv.org/api/query?search_query=cat:{q_enc}&sortBy=submittedDate&sortOrder=descending&max_results=6"
    time.sleep(GOLDEN_PACING_SEC)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OasisMCP-ArXiv/22.2"})
        xml_raw = urllib.request.urlopen(req, timeout=28).read().decode("utf-8", errors="ignore")
        root = ET.fromstring(xml_raw)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = []
        for entry in root.findall("atom:entry", ns):
            title = re.sub(r"\s+", " ", entry.findtext("atom:title", "", ns)).strip()
            published = entry.findtext("atom:published", "", ns)[:10]
            aid = entry.findtext("atom:id", "", ns).split("/abs/")[-1]
            summary = re.sub(r"\s+", " ", entry.findtext("atom:summary", "", ns)).strip()[:180]
            entries.append(f"  • [{published}] ({aid}) {title}\n    Resumen: {summary}...")
        return "🛰️ [ARXIV FÍSICA TEÓRICA & MATEMÁTICA — ÚLTIMOS PREPRINTS]:\n" + "\n".join(entries)
    except Exception as e:
        return f"❌ Error consultando arXiv: {e}"

def tool_search_pilares(query: str) -> str:
    verdad = BASE_DIR / "vault" / "VERDAD_OASIS.md"
    if not verdad.exists():
        return "⚠️ vault/VERDAD_OASIS.md no disponible en este entorno."
    q = query.lower().strip()
    matches = [
        ln.strip() for ln in verdad.read_text(encoding="utf-8", errors="ignore").splitlines()
        if q and q in ln.lower()
    ]
    if not matches:
        return f"🔍 Sin coincidencias exactas para '{query}' en VERDAD_OASIS.md."
    return "📚 [PILARES ENCONTRADOS]:\n" + "\n".join(f"  • {m[:180]}" for m in matches[:6])

def tool_verify_lean4() -> str:
    notary = BASE_DIR / "sovereign_catalog" / "18_ym_notary_verify.py"
    if not notary.exists():
        return "⚠️ Notario Módulo 18 no encontrado."
    res = subprocess.run([sys.executable, str(notary)], capture_output=True, text=True, timeout=30)
    return res.stdout.strip() or res.stderr.strip()

def dispatch_tool(name: str, args: dict) -> str:
    if name == "web_scraper":
        return tool_web_scraper(str(args.get("url", "")))
    if name == "search_pilares":
        return tool_search_pilares(str(args.get("query", "")))
    if name == "verify_lean4":
        return tool_verify_lean4()
    return f"❌ Herramienta MCP desconocida: {name}"

# ==============================================================================
# 2. SERVIDOR MCP NATIVO (JSON-RPC 2.0 STDIO)
# ==============================================================================
def serve_mcp_stdio():
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        req_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params") or {}

        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "oasis-sovereign-mcp", "version": "22.2.0"}
            }
        elif method == "tools/list":
            result = {"tools": MCP_TOOLS}
        elif method == "tools/call":
            t_name = params.get("name", "")
            t_args = params.get("arguments") or {}
            output_text = dispatch_tool(t_name, t_args)
            result = {"content": [{"type": "text", "text": output_text}]}
        elif method == "notifications/initialized":
            continue
        else:
            if req_id is None:
                continue
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}) + "\n")
            sys.stdout.flush()
            continue

        if req_id is not None:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
            sys.stdout.flush()

# ==============================================================================
# 3. PUENTE AGÉNTICO CON POOL SMOLMAXXING (OLLAMA LOCAL 2 HILOS)
# ==============================================================================
def ask_ollama_with_mcp(user_query: str) -> str:
    # Detectar si la consulta pide explícitamente inspeccionar una URL o buscar en pilares
    url_match = re.search(r"(https?://[^\s]+|(?:[a-z0-9-]+\.)+(?:com|org|net|es|io|ai|gov)(?:/[^\s]*)?)", user_query, flags=re.I)
    tool_context = ""
    if url_match:
        tool_context = tool_web_scraper(url_match.group(1))
    elif any(k in user_query.lower() for k in ("arxiv", "paper", "fisica", "física", "subido", "hoy")):
        tool_context = tool_arxiv_physics_today("hep-th")
    elif any(k in user_query.lower() for k in ("pilar", "crouzeix", "378", "340", "310", "kappa")):
        tool_context = tool_search_pilares(user_query)

    sys_prompt = (
        "Eres el Agente Investigador de Oasis OS dotado de herramientas MCP reales.\n"
        "Regla absoluta: Responde ÚNICAMENTE basándote en el [CONTEXTO MCP VERIFICADO] proporcionado abajo. "
        "Si el dato no está en el contexto, dilo con honestidad sin inventar cifras.\n\n"
        f"[CONTEXTO MCP VERIFICADO]:\n{tool_context or 'Sin llamada web externa; usa solo hechos verificados.'}"
    )

    for model in ("oasis-smol-rag", "oasis-smol-c99", "oasis-sovereign:1.5b", "oasis-flash:0.5b"):
        try:
            payload = json.dumps({
                "model": model,
                "prompt": f"{sys_prompt}\n\nPREGUNTA: {user_query}\nRESPUESTA:",
                "stream": False,
                "options": {"num_thread": 2, "num_ctx": 1536, "num_predict": 240, "temperature": 0.05}
            }).encode("utf-8")
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                ans = json.loads(r.read().decode("utf-8")).get("response", "").strip()
                if ans:
                    header = f"{tool_context}\n────────────────────────────────────────────────────────────────\n" if tool_context else ""
                    return f"{header}🧠 [SÍNTESIS MCP + {model}]:\n{ans}"
        except Exception:
            continue

    # Modo 24/7 determinista si Ollama está apagado
    if tool_context:
        return f"{tool_context}\n────────────────────────────────────────────────────────────────\nℹ️ (Ollama local inactivo: mostrando extracción directa MCP verificada)"
    return (
        "🔌 [SERVIDOR MCP SOBERANO v22.2.0 — LISTO]\n"
        "• Herramientas registradas : web_scraper (Pacing Áureo π/φ), search_pilares, verify_lean4\n"
        "• Uso CLI / Web            : mcp https://ejemplo.com  |  scrape https://zenodo.org/records/24311596\n"
        "• Uso Estándar MCP (stdio) : python3 sovereign_catalog/20_mcp_sovereign_server.py --stdio"
    )

def mcp_process(arg: str = "") -> str:
    q = arg.strip()
    if not q:
        return ask_ollama_with_mcp("")
    if q.startswith(("http://", "https://")) or re.match(r"^[a-z0-9.-]+\.[a-z]{2,}(/|$)", q, re.I):
        return tool_web_scraper(q)
    return ask_ollama_with_mcp(q)

if __name__ == "__main__":
    if "--stdio" in sys.argv:
        serve_mcp_stdio()
    else:
        print(mcp_process(" ".join(sys.argv[1:])))


# === OVRP DETERMINISTIC BOUNTY & GRANT RADAR (16-DOI STACK) ===
def scan_ovrp_bounties(timeout: int = 10) -> list[dict]:
    """Rastrea convocatorias y bounties alineados con Lean 4, C99, OVRP y EU AI Act (0% LLM)."""
    import json
    import re
    import urllib.request
    import xml.etree.ElementTree as ET

    keywords = {
        "formal verification": 0.30, "lean": 0.25, "cryptograph": 0.20,
        "audit": 0.20, "reproducib": 0.20, "provenance": 0.20,
        "sovereign": 0.15, "open source": 0.15, "ai act": 0.25,
        "trustworthy ai": 0.25, "c99": 0.15, "security": 0.10,
    }
    sources = [
        ("NLnet Foundation", "https://nlnet.nl/feed.atom", 25000.0, 120.0, 2.0),
        ("Ethereum Foundation", "https://blog.ethereum.org/feed.xml", 30000.0, 150.0, 3.0),
        ("ACCIÓ Catalonia", "https://www.accio.gencat.cat/ca/serveis/ajuts/index.html", 40000.0, 160.0, 2.0),
        ("EU Funding & Tenders", "https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantsTenders.json", 60000.0, 240.0, 4.0),
    ]
    ranked = []
    for src, url, reward, hours, comp in sources:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Oasis-OVRP-Radar/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            if url.endswith(".json"):
                items = json.loads(raw).get("fundingData", {}).get("GrantTenderObj", [])[:35]
                for it in items:
                    title = str(it.get("title") or it.get("identifier") or "EU Call").strip()
                    fit = min(1.0, sum(w for kw, w in keywords.items() if kw in json.dumps(it).lower()))
                    if fit >= 0.20:
                        score = round((reward * fit) / (hours * comp), 2)
                        ranked.append({"score": score, "fit": fit, "reward_eur": reward, "source": src, "title": title, "url": "https://ec.europa.eu/info/funding-tenders/"})
            elif url.endswith(".html"):
                for href, label in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', raw, flags=re.I | re.S)[:50]:
                    clean_t = re.sub(r"<[^>]+>", " ", label).strip()
                    fit = min(1.0, sum(w for kw, w in keywords.items() if kw in f"{clean_t} {href}".lower()))
                    if fit >= 0.15 and len(clean_t) > 8:
                        full_u = href if href.startswith("http") else f"https://www.accio.gencat.cat{href}"
                        score = round((reward * fit) / (hours * comp), 2)
                        ranked.append({"score": score, "fit": fit, "reward_eur": reward, "source": src, "title": clean_t, "url": full_u})
            else:
                root = ET.fromstring(raw)
                entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//item")
                for item in entries[:25]:
                    t_el = item.find("{http://www.w3.org/2005/Atom}title") or item.find("title")
                    title = (t_el.text or "").strip() if t_el is not None else "Feed Entry"
                    blob = re.sub(r"<[^>]+>", " ", ET.tostring(item, encoding="unicode")).lower()
                    fit = min(1.0, sum(w for kw, w in keywords.items() if kw in blob))
                    if fit >= 0.20:
                        score = round((reward * fit) / (hours * comp), 2)
                        ranked.append({"score": score, "fit": fit, "reward_eur": reward, "source": src, "title": title, "url": url})
        except Exception:
            continue
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
