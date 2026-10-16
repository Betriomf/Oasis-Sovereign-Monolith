#!/usr/bin/env python3
import os, json

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
BUZON = os.path.join(MONOLITH_DIR, "data/lincos_db/buzon_agentes.json")

print("🎨 [PASO 2 - VELÁZQUEZ]: Estructurando literatura externa en Lincos / Lean 4...")

with open(BUZON, "r", encoding="utf-8") as f:
    datos = json.load(f)

articulos = datos.get("articulos", [])

trama = "⟨LINCOS::EXTERNAL_NAVIER_PAPERS⟩\n"
for a in articulos:
    trama += f"• TITULO: {a['titulo']}\n"
    trama += f"  EXTRACTO: {a['resumen']}\n"

trama_pi = trama[:3141]

datos_out = {
    "etapa": 2,
    "agente": "Velázquez",
    "tamano_bytes": len(trama_pi.encode("utf-8")),
    "trama_lincos": trama_pi,
    "estado": "LISTO_PARA_AETHER_LEAN4"
}

with open(BUZON, "w", encoding="utf-8") as f:
    json.dump(datos_out, f, indent=2, ensure_ascii=False)

print(f"✅ [VELÁZQUEZ]: Trama Lincos preparada ({len(trama_pi.encode('utf-8'))} bytes) para deducción en Lean 4.")
