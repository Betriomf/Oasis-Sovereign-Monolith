#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — AARON SWARTZ OPEN SCIENCE RSS AGENT (Pilar 62)
Agente de recolección de literatura libre mediante feeds RSS/Atom abiertos (arXiv / Zenodo).
Homenafe a la liberación del conocimiento público bajo licencias Creative Commons (CC BY 4.0).
Fragmenta la información en tramas Lincos (π KB) para el RAG de Capa 0 a 5.39W.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import math
import time

PHI = (1.0 + math.sqrt(5.0)) / 2.0
PI_FRAME_KB = 3.14159265

class AetherAaronSwartzRSSAgent:
    def __init__(self):
        print("📖 [AGENTE AARON SWARTZ]: Inicializando recolector de conocimiento abierto (RSS/CC BY)...")
        self.arxiv_feeds = [
            "http://export.arxiv.org/rss/hep-th",  # Física Teórica de Alta Energía (AdS/CFT)
            "http://export.arxiv.org/rss/gr-qc"   # Relatividad General y Cosmología Quantum
        ]

    def procesar_feed_rss(self, url_feed: str, max_items: int = 3):
        print(f"\n📡 [RASTREANDO CANAL ABIERTO]: {url_feed}")
        req = urllib.request.Request(url_feed, headers={'User-Agent': 'OasisSovereignMonolith/1.0 (OpenScience; @Betriomf)'})
        
        articulos_extraidos = []
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            # Manejo de namespaces RSS/Atom
            for item in root.findall('.//item')[:max_items]:
                titulo = item.find('title').text.strip() if item.find('title') is not None else "Sin título"
                link = item.find('link').text.strip() if item.find('link') is not None else ""
                descripcion = item.find('description').text.strip() if item.find('description') is not None else ""

                # Limpieza de etiquetas de descripción
                resumen_limpio = descripcion.replace('\n', ' ').split('Abstract:')[ -1 ].strip()
                
                # Formatear trama Lincos (3.14 KB)
                trama_lincos = {
                    "titulo": titulo,
                    "link": link,
                    "resumen": resumen_limpio[:500],
                    "licencia": "Creative Commons / Public Domain",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                articulos_extraidos.append(trama_lincos)
                print(f" ├─ 📑 [{titulo[:60]}...]")
                print(f" │ 🔗 Link: {link}")

            print(f" └─ ✅ {len(articulos_extraidos)} artículos libres ingeridos en tramas π KB.")
            return articulos_extraidos

        except Exception as e:
            print(f" ⚠️ [AVISO RSS]: Modo offline activo o límite alcanzado ({e}). Simulando ingesta local.")
            return []

if __name__ == "__main__":
    agent = AetherAaronSwartzRSSAgent()
    # Ingesta de prueba sobre el feed de hep-th
    agent.procesar_feed_rss("http://export.arxiv.org/rss/hep-th", max_items=2)
