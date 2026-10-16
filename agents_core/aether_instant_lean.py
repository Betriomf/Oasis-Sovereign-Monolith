#!/usr/bin/env python3
"""
OASIS — INFERENCIA ULTRA-RÁPIDA LEAN 4 (MODELO LIGERO LOCAL)
Utiliza modelos sub-1GB para evitar contención de memoria en 8GB de RAM.
"""
import os, json, sys, time, urllib.request

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
BUZON = os.path.join(MONOLITH_DIR, "data/lincos_db/buzon_agentes.json")

print("🌌 [AGENTE ÆTHER]: Iniciando inferencia en silicio frío...")

with open(BUZON, "r", encoding="utf-8") as f:
    datos = json.load(f)

trama = datos.get("trama_lincos", "")

# Modelo de 397 MB: entra holgado en la RAM libre
MODELO = "qwen2.5:0.5b"

prompt = (
    "SYSTEM: Responde SOLO con código Lean 4 formal. Cero prosa.\n\n"
    f"{trama}\n\n"
    "Escribe el teorema 'navier_stokes_helical_regularity' en Lean 4 con sorry.\n"
    "Lean 4 Code:\n"
)

payload = {
    "model": MODELO,
    "prompt": prompt,
    "stream": True,
    "options": {
        "temperature": 0.05,
        "num_predict": 180,
        "num_thread": 2,
        "num_ctx": 512
    }
}

req = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print(f"⚡ [TRANSMISIÓN EN VIVO DESDE {MODELO}]:")
print("=" * 70)
acumulado = []
t0 = time.time()

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        for line in resp:
            if line:
                chunk = json.loads(line.decode("utf-8"))
                tok = chunk.get("response", "")
                sys.stdout.write(tok)
                sys.stdout.flush()
                acumulado.append(tok)
                if chunk.get("done", False):
                    break
    print("\n" + "=" * 70)
    respuesta = "".join(acumulado).strip()
    metodo = f"NEURONAL_LOCAL_{MODELO}"
except Exception as e:
    print(f"\n⚠️ Error local: {e}")
    sys.exit(1)

tiempo = round(time.time() - t0, 2)
datos["lean4_code"] = respuesta
datos["tiempo_s"] = tiempo
datos["metodo"] = metodo
datos["modelo_usado"] = MODELO

with open(BUZON, "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)

print(f"✅ Respuesta neuronal viva depositada en el buzón ({tiempo} s).")
