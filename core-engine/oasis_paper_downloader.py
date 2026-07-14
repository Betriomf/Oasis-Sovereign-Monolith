#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 📡 OASIS SCIBOT: EXTRACTOR SOBERANO DE PAPERS CIENTÍFICOS

import os
import requests
import re

print("🚀 Inicializando SciBot Oasis (Capa 0)...")

def descargar_paper_scihub(doi, output_filename):
    # Usamos un mirror activo estable de Sci-Hub
    SCIHUB_URL = "https://sci-hub.ru/"
    target_url = f"{SCIHUB_URL}{doi}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        print(f"🔍 Escaneando Lattice en busca del DOI: {doi}")
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Buscar el enlace al PDF embebido en el HTML mediante Regex
            pdf_match = re.search(r'src=["\'](//dacemirror[^"\']+\.pdf)', response.text)
            if not pdf_match:
                pdf_match = re.search(r'location\.href=["\']([^"\']+\.pdf)', response.text)
                
            if pdf_match:
                pdf_url = pdf_match.group(1)
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                
                print(f"📥 Flujo laminar detectado. Descargando PDF desde: {pdf_url}")
                pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
                
                # Crear el directorio de almacenamiento en frío si no existe
                os.makedirs("~/Oasis_Historico/Papers", exist_ok=True)
                path_final = os.path.expanduser(f"~/Oasis_Historico/Papers/{output_filename}")
                
                with open(path_final, "wb") as f:
                    f.write(pdf_response.content)
                
                print(f"💎 PAPERS_CLOSED: Sincronizado con éxito en {path_final}")
                return True
            else:
                print("⚠️ Jitter detectado: Captcha activo o paper no indexado en este mirror.")
        else:
            print(f"❌ Error de respuesta en la aduana Sci-Hub: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Falla crítica en el bus de descarga: {e}")
    return False

if __name__ == "__main__":
    # DOI de prueba: Un paper clásico de física/cosmología de Nature
    doi_ejemplo = "10.1038/nature09492"
    descargar_paper_scihub(doi_ejemplo, "nature_hubble_base.pdf")
