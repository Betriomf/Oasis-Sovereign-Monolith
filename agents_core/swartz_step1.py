#!/usr/bin/env python3
import os, json, re, glob

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
DB_DIR = os.path.join(MONOLITH_DIR, "data/lincos_db")
os.makedirs(DB_DIR, exist_ok=True)
BUZON = os.path.join(DB_DIR, "buzon_agentes.json")

print("📚 [PASO 1 - AARON SWARTZ]: Rastreando literatura y pilares de Navier-Stokes...")

pilares_encontrados = []
truth_file = os.path.join(MONOLITH_DIR, "VERDAD_OASIS.txt")
if os.path.exists(truth_file):
    with open(truth_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if any(k in line.lower() for k in ["navier", "enstrof", "bkm", "quiral", "besov", "pilar 201", "pilar 339"]):
                pilares_encontrados.append(line.strip())

docs_encontrados = []
for dp in glob.glob(os.path.join(MONOLITH_DIR, "docs/*NAVIER*.md")) + glob.glob(os.path.join(MONOLITH_DIR, "docs/*PILAR_201*.md")):
    with open(dp, "r", encoding="utf-8", errors="ignore") as f:
        matches = re.findall(r"(?:Lema|Teorema|Proposition).*?\n", f.read(), re.IGNORECASE)
        docs_encontrados.append({"doc": os.path.basename(dp), "extractos": matches[:2]})

datos_etapa1 = {
    "etapa": 1,
    "agente": "Aaron Swartz",
    "total_pilares": len(pilares_encontrados),
    "pilares": pilares_encontrados[:8],
    "documentos": docs_encontrados[:4]
}

with open(BUZON, "w", encoding="utf-8") as f:
    json.dump(datos_etapa1, f, indent=2, ensure_ascii=False)

print(f"✅ [AARON SWARTZ]: {len(pilares_encontrados)} pilares y {len(docs_encontrados)} documentos depositados en el buzón.")
print(f"📍 Salida guardada en: {BUZON}")
