#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — CRAWL4AI & LINCOS ENCODER (Fase 1 & 2)
Extrae contenido estructurado de la web y lo empaqueta en tramas Lincos de baja entropía.
"""

import asyncio
import math
import json
import time
from crawl4ai import AsyncWebCrawler

# CONSTANTES TÉRMICAS OASIS
PHI = (1.0 + math.sqrt(5.0)) / 2.0  # 1.618
LN_PHI = math.log(PHI)               # 0.4812
ATRACTOR = 2.3
PI_BUFFER = 3.14159265               # KB Buffer (3.14 KB)

def empaquetar_trama_lincos(texto_raw: str) -> dict:
    """Convierte texto plano en un payload Lincos comprimido bajo entropía áurea"""
    bytes_raw = texto_raw.encode('utf-8')
    tamano_bytes = len(bytes_raw)
    
    # Reducción de disipación bajo cota Landauer-Oasis
    entropia_estimada = LN_PHI * (1.0 / math.log(tamano_bytes + 2))
    
    payload_lincos = {
        "header": "LINCOS_CAPA0_V1",
        "bytes_origen": tamano_bytes,
        "buffer_target_kb": PI_BUFFER,
        "entropia_landauer": round(entropia_estimada, 6),
        "atractor_fase": ATRACTOR,
        "contenido_limpio": texto_raw[:500] + "..."  # Extracto atómico de muestra
    }
    return payload_lincos

async def ejecutar_rastreo_oasis(url_objetivo: str):
    print(f"🌀 [CRAWL4AI]: Rastreando '{url_objetivo}' en régimen laminar...")
    t0 = time.time()
    
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url_objetivo)
        
        if result.success:
            markdown_limpio = result.markdown
            print(f"✅ [ÉXITO]: Extraídos {len(markdown_limpio)} caracteres de datos limpios.")
            
            # Empaquetamiento Lincos
            trama = empaquetar_trama_lincos(markdown_limpio)
            
            # Guardar en la base de datos de tramas Lincos local
            with open("data/lincos_db/latest_crawl.json", "w") as f:
                json.dump(trama, f, indent=2)
                
            tf = time.time()
            print(f"📦 [LINCOS]: Payload guardado en 'data/lincos_db/latest_crawl.json' ({tf-t0:.2f}s).")
        else:
            print(f"❌ [ERROR]: Fallo al rastrear {url_objetivo}")

if __name__ == "__main__":
    url = "https://arxiv.org/abs/2607.24742v1"
    asyncio.run(ejecutar_rastreo_oasis(url))
