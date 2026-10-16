#!/usr/bin/env python3
import os, json

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
DB_DIR = os.path.join(MONOLITH_DIR, "data/lincos_db")
BUZON = os.path.join(DB_DIR, "buzon_agentes.json")
PI_FRAME_LIMIT = 3141  # Límite formal π-KB Oasis

print("🎨 [PASO 2 - AGENTE VELÁZQUEZ]: Leyendo buzón asíncrono de Aaron Swartz...")

if not os.path.exists(BUZON):
    print("❌ Error: El buzón no contiene datos de la Etapa 1.")
    exit(1)

with open(BUZON, "r", encoding="utf-8") as f:
    datos_in = json.load(f)

# Estructurar la síntesis óptica en gramática Lincos pura
cuerpo = "⟨LINCOS::CORPUS_NAVIER_STOKES_CONFINED⟩\n"
cuerpo += "⟨AXIOMS::PILAR_CORPUS⟩\n"
for p in datos_in.get("pilares", [])[:6]:
    cuerpo += f"  • {p}\n"

cuerpo += "⟨LEMMAS::FORMAL_DOCS⟩\n"
for d in datos_in.get("documentos", []):
    cuerpo += f"  • Doc: {d['doc']} | " + " // ".join(d['extractos']) + "\n"

# Confinar estrictamente al contenedor esférico de π KB
trama_pi = cuerpo[:PI_FRAME_LIMIT]

datos_etapa2 = {
    "etapa": 2,
    "agente": "Velázquez",
    "tamano_bytes": len(trama_pi.encode("utf-8")),
    "trama_lincos": trama_pi,
    "estado": "EN_CONTENEDOR_PI_KB"
}

with open(BUZON, "w", encoding="utf-8") as f:
    json.dump(datos_etapa2, f, indent=2, ensure_ascii=False)

print(f"✅ [VELÁZQUEZ]: Trama Lincos empaquetada con éxito ({len(trama_pi.encode('utf-8'))} bytes).")
print("📦 Contenedor esférico π-KB sellado en el buzón para el Agente ÆTHER.")
