#!/usr/bin/env python3
"""
OASIS PAPER AGENT — Búsqueda de literatura científica reciente (arXiv API)
Filtra artículos en física de la información, AdS/CFT y protocolos P2P.
"""
import urllib.request
import xml.etree.ElementTree as ET

QUERIES = [
    "Landauer+limit+information",
    "holographic+principle+computation",
    "low+bandwidth+mesh+protocol"
]

def buscar_articulos():
    print("🔭 [OASIS AGENT]: Consultando repositorios científicos (arXiv)...")
    print("=" * 70)

    for query in QUERIES:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=2&sortBy=submittedDate&sortOrder=descending"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            print(f"\n📑 Resultados para categoría: '{query.replace('+', ' ')}'")
            print("-" * 70)

            for entry in root.findall('atom:entry', ns):
                titulo = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                publicado = entry.find('atom:published', ns).text[:10]
                link = entry.find('atom:id', ns).text

                print(f"📌 [{publicado}] {titulo}")
                print(f"   🔗 Link: {link}\n")

        except Exception as e:
            print(f"⚠️ Error en la consulta '{query}': {e}")

if __name__ == "__main__":
    buscar_articulos()
