#!/usr/bin/env python3
"""
Oasis Sovereign Monolith — Autonomous Outreach & RSS Sync
Regenera outreach/feed.xml y outreach/index.html directamente desde
vault/zenodo_classified_catalog.json (0% CPU LLM, 0 tokens requeridos).
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CAT_PATH = ROOT / "vault" / "zenodo_classified_catalog.json"
OUT_DIR = ROOT / "outreach"

KEYWORDS = ("folding", "proteostasis", "atp", "crowding", "chaperone", "pdb")

def main() -> None:
    if not CAT_PATH.exists():
        raise SystemExit(f"❌ No existe {CAT_PATH}")

    cat_data = json.loads(CAT_PATH.read_text(encoding="utf-8"))
    records = cat_data.get("records", [])

    selected = []
    for r in records:
        if r.get("state") != "published":
            continue
        title = r.get("title", "")
        t_low = title.lower()
        if any(k in t_low for k in KEYWORDS):
            rid = str(r.get("id", ""))
            doi = r.get("doi") or f"10.5281/zenodo.{rid}"
            selected.append({
                "id": rid,
                "doi": doi,
                "title": title,
                "date": r.get("date", "2026-11-27"),
                "license": str(r.get("license", "CC-BY-SA-4.0")).lower(),
                "url": f"https://doi.org/{doi}",
            })

    selected.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else 0, reverse=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now_rfc = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    items_xml = []
    cards_html = []
    for item in selected:
        items_xml.append(
            f"""    <item>
      <title>{escape(item['title'])}</title>
      <link>{escape(item['url'])}</link>
      <guid isPermaLink="true">{escape(item['url'])}</guid>
      <pubDate>{now_rfc}</pubDate>
      <description>{escape(item['title'])} — Verified under OVRP (Lean 4 + C99 + Bitcoin OTS), License: {escape(item['license'])}.</description>
    </item>"""
        )
        cards_html.append(
            f"""    <article class="card">
      <h2><a href="{escape(item['url'])}" target="_blank" rel="noopener">{escape(item['title'])}</a></h2>
      <div><span class="tag">{escape(item['license'].upper())}</span> <span class="meta">{escape(item['date'])}</span> · DOI: <code>{escape(item['doi'])}</code></div>
    </article>"""
        )

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Oasis Sovereign Research — Protein Folding &amp; Proteostasis Series</title>
    <link>https://github.com/Betriomf/Oasis-Sovereign-Monolith</link>
    <description>Open-access, formally verified computational biophysics and informational thermodynamics working papers (CC-BY-SA-4.0 / AGPL-3.0).</description>
    <lastBuildDate>{now_rfc}</lastBuildDate>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""

    index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Oasis Sovereign Research — Protein Folding &amp; Proteostasis Series</title>
  <link rel="alternate" type="application/rss+xml" title="Oasis Proteostasis RSS" href="./feed.xml" />
  <style>
    :root {{ --bg: #0d1117; --card: #161b22; --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --badge: #238636; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); max-width: 900px; margin: 2rem auto; padding: 0 1.2rem; line-height: 1.6; }}
    header {{ border-bottom: 1px solid #30363d; padding-bottom: 1.2rem; margin-bottom: 1.8rem; }}
    h1 {{ font-size: 1.55rem; margin: 0 0 0.4rem 0; }}
    .meta {{ color: var(--muted); font-size: 0.90rem; }}
    .actions {{ margin-top: 1rem; display: flex; gap: 0.8rem; flex-wrap: wrap; }}
    .btn {{ display: inline-block; padding: 0.45rem 0.9rem; border-radius: 6px; text-decoration: none; font-size: 0.88rem; font-weight: 600; }}
    .btn-rss {{ background: #da6d10; color: #fff; }}
    .btn-gh {{ background: #21262d; color: var(--text); border: 1px solid #30363d; }}
    .card {{ background: var(--card); border: 1px solid #30363d; border-radius: 8px; padding: 1.05rem 1.3rem; margin-bottom: 0.95rem; }}
    .card h2 {{ font-size: 1.05rem; margin: 0 0 0.4rem 0; }}
    .card a {{ color: var(--accent); text-decoration: none; }}
    .card a:hover {{ text-decoration: underline; }}
    .tag {{ display: inline-block; background: var(--badge); color: #fff; font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 4px; margin-right: 0.4rem; }}
    footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #30363d; color: var(--muted); font-size: 0.85rem; }}
  </style>
</head>
<body>
  <header>
    <h1>Oasis Sovereign Research — Protein Folding &amp; Proteostasis Series ({len(selected)} Publications)</h1>
    <div class="meta">Mariano Panzano Caballé · Oasis Verifiable Research Pipeline (OVRP: Lean 4.36.0 + C99 + SHA-256 + Bitcoin OTS)</div>
    <div class="actions">
      <a class="btn btn-rss" href="./feed.xml">📡 Suscribirse al Canal RSS (feed.xml)</a>
      <a class="btn btn-gh" href="https://github.com/Betriomf/Oasis-Sovereign-Monolith" target="_blank" rel="noopener">⚙️ Repositorio GitHub (Lean 4 &amp; C99)</a>
    </div>
  </header>
  <main>
{chr(10).join(cards_html)}
  </main>
  <footer>
    Generado automáticamente por <code>tools/oasis_outreach_sync.py</code>. Modelos fenomenológicos verificados formalmente; no constituyen protocolos clínicos.
  </footer>
</body>
</html>
"""

    (OUT_DIR / "feed.xml").write_text(rss_xml, encoding="utf-8")
    (OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"✅ Outreach sincronizado ({len(selected)} publicaciones): outreach/feed.xml y outreach/index.html actualizados.")

if __name__ == "__main__":
    main()
