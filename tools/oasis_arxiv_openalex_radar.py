#!/usr/bin/env python3
"""
[OASIS ACADEMIC API RADAR — ARXIV & OPENALEX]
Consulta las APIs oficiales de arXiv y OpenAlex para localizar preprints recientes
sobre Yang-Mills 4D, brecha de masa y formalización en Lean 4.
"""
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 8):
    encoded = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={encoded}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    req = urllib.request.Request(url, headers={"User-Agent": "Oasis-Research-Radar/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        xml_data = resp.read()
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("atom:entry", ns):
        title = " ".join(entry.find("atom:title", ns).text.split())
        published = entry.find("atom:published", ns).text[:10]
        link = entry.find("atom:id", ns).text
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        results.append((published, title, authors[:3], link))
    return results

def search_openalex(search_term: str, per_page: int = 8):
    encoded = urllib.parse.quote(search_term)
    url = f"https://api.openalex.org/works?search={encoded}&sort=publication_date:desc&per-page={per_page}"
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:research@oasis-sovereign.org"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for w in data.get("results", []):
        title = w.get("title", "Sin título")
        date = w.get("publication_date", "N/A")
        doi = w.get("doi") or w.get("id")
        results.append((date, title, doi))
    return results

if __name__ == "__main__":
    print("=================================================================")
    print("🔭 ARXIV API — ÚLTIMOS PREPRINTS (YANG-MILLS / MASS GAP / LEAN)")
    print("=================================================================")
    for pub, title, authors, link in search_arxiv('all:"Yang-Mills" AND (all:"mass gap" OR all:"Lean")', 8):
        print(f"  [{pub}] {title}\n     Autores: {', '.join(authors)} | {link}")

    print("\n=================================================================")
    print("📚 OPENALEX API — INDEXACIÓN GLOBAL RECIENTE")
    print("=================================================================")
    for pub, title, doi in search_openalex("Yang-Mills mass gap constructive Lean 4", 8):
        print(f"  [{pub}] {title}\n     Ref: {doi}")
