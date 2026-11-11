#!/usr/bin/env python3
"""
OASIS TECH INDEXER — MAPEADOR CATEGÓRICO DE CAPA 0
Analiza vault/OASIS_FULL_CODE.md y construye vault/oasis_tech_index.json
asociando cada archivo a categorías: C99/Silicio, IA/SLMs, Bóveda/OPFS, Redes/LoRa, UI/DualXterm y Física.
"""
import os
import json
import re
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL_CODE_PATH = os.path.join(BASE_DIR, "vault", "OASIS_FULL_CODE.md")
INDEX_JSON_PATH = os.path.join(BASE_DIR, "vault", "oasis_tech_index.json")

TAXONOMY = {
    "silicio_c99": {
        "label": "C99 SIMD & Micronúcleo",
        "keywords": ["c99", "simd", "avx2", "fma", "mach_absolute_time", "lean 4", "sorry = 0", "posix", "fhs"]
    },
    "ia_slm_rag": {
        "label": "Modelos SLM & Inferencia Laminar",
        "keywords": ["ollama", "qwen:flash", "qwen2.5", "aether", "phi3", "pilar 190", "pi-kb", "sse", "stream"]
    },
    "cripto_boveda": {
        "label": "Criptografía & Bóveda Local-First",
        "keywords": ["opfs", "syncaccesshandle", "aes-256-gcm", "webcrypto", "bohr-hafnium", "zeroizacion", "soulbound", "did:key"]
    },
    "redes_p2p_lora": {
        "label": "Redes Malla & Telecomunicaciones",
        "keywords": ["pacing áureo", "pi/phi", "gossip", "golod-shafarevich", "o-quic", "webrtc", "minkowski", "lincos", "lora", "dora"]
    },
    "interfaz_dualxterm": {
        "label": "Frontend & DualXterm UI",
        "keywords": ["dualxterm", "xterm.js", "root@oasis-hurd", "host@darwin", "webgl", "canvas", "three.js", "hud"]
    },
    "fisica_termodinamica": {
        "label": "Física Teórica & Navier-Stokes",
        "keywords": ["landauer", "silicio frío", "enstrofia", "kappa = ln 10", "pilar 378", "bkm", "blow-up", "fibonacci"]
    }
}

def generate_index():
    if not os.path.exists(FULL_CODE_PATH):
        print(f"Error: {FULL_CODE_PATH} no existe. Ejecuta primero oasis_scraper_engine.py --code.")
        return

    print("🔍 [INDEXER]: Mapeando 2641 archivos contra la taxonomía tecnológica de Oasis...")
    t0 = time.perf_counter()

    file_blocks = {}
    current_file = None
    lines_buffer = []

    with open(FULL_CODE_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("# ARCHIVO: "):
                if current_file and lines_buffer:
                    file_blocks[current_file] = "\n".join(lines_buffer)
                current_file = line.replace("# ARCHIVO: ", "").strip()
                lines_buffer = []
            else:
                if current_file:
                    lines_buffer.append(line)
        if current_file and lines_buffer:
            file_blocks[current_file] = "\n".join(lines_buffer)

    tech_index = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_files_scanned": len(file_blocks),
        "categories": {}
    }

    for cat_id, cat_info in TAXONOMY.items():
        tech_index["categories"][cat_id] = {
            "name": cat_info["label"],
            "matched_files_count": 0,
            "files": []
        }
        for fname, text in file_blocks.items():
            text_lower = text.lower()
            matched_kw = [kw for kw in cat_info["keywords"] if kw in text_lower]
            if matched_kw:
                tech_index["categories"][cat_id]["files"].append({
                    "file": fname,
                    "matched_keywords": matched_kw,
                    "matches_count": len(matched_kw)
                })
        
        # Ordenar archivos por relevancia
        tech_index["categories"][cat_id]["files"].sort(key=lambda x: x["matches_count"], reverse=True)
        tech_index["categories"][cat_id]["matched_files_count"] = len(tech_index["categories"][cat_id]["files"])

    with open(INDEX_JSON_PATH, "w", encoding="utf-8") as out:
        json.dump(tech_index, out, indent=2, ensure_ascii=False)

    t_total = time.perf_counter() - t0
    print(f"✅ [INDEXER COMPLETADO]: Índice guardado en {INDEX_JSON_PATH} en {t_total:.2f} s.")
    for cat_id, data in tech_index["categories"].items():
        print(f"  • {data['name']:<35}: {data['matched_files_count']} archivos vinculados")

if __name__ == "__main__":
    generate_index()
