#!/usr/bin/env python3
import json, urllib.request

prompt = (
    "[SISTEMA OASIS OS - CAPA 0 HÍBRIDA & LEAN 4 INTEGRADO]:\n"
    "• Modulo Formal Cargado: KozonoTaniuchiLogBound.lean\n"
    "• Cota Integrada: ||∇u||_{L^∞} ≤ C (1 + ||ω||_{Ḃ⁰_{∞,∞}} * ln(1 + ||u||_{Hˢ}))\n"
    "• Estado Térmico: RÉGIMEN_ADIABÁTICO_<=_4.18W (Silicio Frío)\n\n"
    "Pregunta: Con el Teorema de Kozono-Taniuchi formally declarado en Lean 4, demuestra cómo "
    "la tasa de crecimiento del término de Besov ||ω||_{Ḃ⁰_{∞,∞}} en la concha diádica j determina "
    "si la cota logarítmica previene el blow-up en tiempo finito T* para datos u₀ ∈ Hˢ(ℝ³) con s > 5/2."
)

payload = {
    "model": "oasis-aether-soup:1.5b",
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.05,
        "num_predict": 1024,
        "num_thread": 2,
        "num_ctx": 2048
    }
}

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("\n🌌 [RESPUESTA DE AETHER SOUP - REGIMEN LAMINAR]:\n")
        print(res.get("response", "").strip())
except Exception as e:
    print(f"🚨 Error de conexión: {e}")
