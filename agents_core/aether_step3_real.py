#!/usr/bin/env python3
import os, json, sys, urllib.request, time

MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
DB_DIR = os.path.join(MONOLITH_DIR, "data/lincos_db")
BUZON = os.path.join(DB_DIR, "buzon_agentes.json")

print("🌌 [PASO 3 REAL - AGENTE ÆTHER]: Conectando con motor neuronal local...")

if not os.path.exists(BUZON):
    print("❌ Error: Buzón vacío.")
    sys.exit(1)

with open(BUZON, "r", encoding="utf-8") as f:
    datos = json.load(f)

trama = datos.get("trama_lincos", "")

# Prompt de deducción directa sin trampa precalculada
prompt = (
    "SYSTEM: Eres ÆTHER, motor analítico en Capa 0. Responde estrictamente con deducción en LaTeX. Cero saludos.\n\n"
    f"CONTEXTO OPERATIVO:\n{trama}\n\n"
    "PREGUNTA:\n"
    "Calcula la derivada d/dt ||w||_{L^2}^2 para Navier-Stokes 3D. "
    "Aplica la descomposición diádica de Littlewood-Paley y deduce si bajo helicidad H(0) > 0 "
    "el término de estiramiento <(w·∇)u, w> queda dominado por la disipación ν 2^{2j}. "
    "Concluye si la cota es condicional o incondicional.\n\n"
    "LaTeX Output:"
)

payload = {
    "model": "qwen2.5:0.5b",
    "prompt": prompt,
    "stream": True,
    "options": {
        "temperature": 0.1,
        "num_predict": 250,
        "num_thread": 2,
        "num_ctx": 1024
    },
    "keep_alive": "10m"
}

req = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("⚡ [ÆTHER]: Inferencia viva en silicio frío (< 5.39W). Generando tokens:\n" + "="*70)
acumulado = []
t0 = time.time()

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        for line in resp:
            if line:
                chunk = json.loads(line.decode("utf-8"))
                tok = chunk.get("response", "")
                sys.stdout.write(tok)
                sys.stdout.flush()
                acumulado.append(tok)
                if chunk.get("done", False):
                    break
    print("\n" + "="*70)
    respuesta_real = "".join(acumulado).strip()
except Exception as e:
    print(f"\n❌ Error en enlace local: {e}")
    sys.exit(1)

# Guardar la deducción real en el buzón
datos_etapa3 = {
    "etapa": 3,
    "agente": "ÆTHER",
    "tiempo_segundos": round(time.time() - t0, 2),
    "deduccion_neuronal_real": respuesta_real,
    "estado": "LISTO_PARA_GOYA"
}

with open(BUZON, "w", encoding="utf-8") as f:
    json.dump(datos_etapa3, f, indent=2, ensure_ascii=False)

print(f"📍 Deducción viva depositada en el buzón ({datos_etapa3['tiempo_segundos']}s).")
