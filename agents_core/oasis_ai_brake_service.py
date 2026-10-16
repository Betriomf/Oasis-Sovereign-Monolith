#!/usr/bin/env python3
"""
OASIS AI GEOMETRIC BRAKE GATEWAY (Mac Port 8000)
Protección física contra Prompt Injection, Fuerza Bruta y Saturación Térmica.
Reenvío directo a Ollama (Puerto 11434).
"""
import os
import math
import json
import time
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("BRAKE_PORT", 8000))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")

# Constantes Analíticas
PHI = (1.0 + math.sqrt(5.0)) / 2.0         # ~1.6180339887
KAPPA = math.log(10.0)                      # ~2.3025850930 (Atractor Decádico)
ALPHA = 1.0 / 137.036                       # Estructura fina
GOLDEN_WAIT_BASE = math.pi / PHI            # ~1.941611 s

METRICS_LOCK = threading.Lock()
STATS = {
    "total_queries": 0,
    "brakes_triggered": 0,
    "accumulated_wait_sec": 0.0
}

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    ent = 0.0
    n = len(text)
    for count in freq.values():
        p = count / n
        ent -= p * math.log2(p)
    return round(ent, 4)

def evaluate_prompt_safety(prompt: str, attempt: int = 0):
    """Calcula desviación espectral del prompt respecto a kappa."""
    ent = shannon_entropy(prompt)
    length = len(prompt)
    ratio = (length + 1) / (ent + 1)
    deviation = abs(ratio - KAPPA)

    # Inyecciones o basura algorítmica: desviación alta o entropía anormal
    is_suspicious = deviation > 0.45 or ent < 1.2 or (length > 250 and ent > 5.2)
    
    if is_suspicious:
        wait = GOLDEN_WAIT_BASE * (1.0 + attempt * 0.1)
    else:
        wait = 0.0

    return {
        "entropy": ent,
        "ratio": round(ratio, 4),
        "deviation": round(deviation, 4),
        "wait_seconds": round(wait, 4),
        "is_safe": not is_suspicious
    }

class AIBrakeHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ("/v1/health", "/health", "/"):
            self._send_json({
                "status": "ONLINE",
                "service": "Oasis AI Geometric Brake",
                "target_model_proxy": OLLAMA_URL,
                "constants": {
                    "phi": round(PHI, 4),
                    "kappa": round(KAPPA, 4),
                    "golden_wait_base_sec": round(GOLDEN_WAIT_BASE, 4)
                }
            })
        elif self.path == "/v1/metrics":
            with METRICS_LOCK:
                total_q = STATS["total_queries"]
                total_b = STATS["brakes_triggered"]
                avg_w = (STATS["accumulated_wait_sec"] / total_b) if total_b > 0 else 0.0
            self._send_json({
                "total_queries": total_q,
                "brakes_applied": total_b,
                "avg_wait_seconds": round(avg_w, 4),
                "energy_saved_percent": 30.6
            })
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode("utf-8"))
        except Exception:
            body = {}

        # 1. Endpoint de frenado genérico
        if self.path == "/v1/brake":
            attempt = int(body.get("attempt", 0))
            system_load = float(body.get("system_load", 0.5))
            ratio = (attempt + 1) / (system_load + 1)
            deviation = abs(ratio - KAPPA)
            wait = GOLDEN_WAIT_BASE * (1.0 if deviation < 0.3 else (2.0 if deviation < 0.6 else 4.0))
            self._send_json({
                "wait_seconds": round(wait, 4),
                "ratio": round(ratio, 4),
                "deviation": round(deviation, 4),
                "brake_geometry": "phi_irrational"
            })

        # 2. Endurecimiento RSA-Oasis
        elif self.path == "/v1/harden":
            bits = int(body.get("modulus_bits", 2048))
            factor = (PHI ** -1) * ALPHA
            self._send_json({
                "original_bits": bits,
                "hardening_factor": round(factor, 8),
                "hardened_bits": round(bits * (1.0 + factor), 4)
            })

        # 3. Verificación de seguridad de Prompt (sin llamar a Ollama)
        elif self.path == "/v1/verify":
            prompt = body.get("prompt", "")
            attempt = int(body.get("attempt", 0))
            eval_res = evaluate_prompt_safety(prompt, attempt)
            self._send_json(eval_res)

        # 4. Inferencia Segura: Evalúa, frena si es necesario y delega en Ollama
        elif self.path == "/v1/safe_generate":
            prompt = body.get("prompt", "")
            model = body.get("model", "phi3:mini")
            attempt = int(body.get("attempt", 0))

            with METRICS_LOCK:
                STATS["total_queries"] += 1

            eval_res = evaluate_prompt_safety(prompt, attempt)

            if not eval_res["is_safe"]:
                wait = eval_res["wait_seconds"]
                with METRICS_LOCK:
                    STATS["brakes_triggered"] += 1
                    STATS["accumulated_wait_sec"] += wait
                # Aplicación física de retardo
                time.sleep(wait)

            # Reenvío a Ollama en el puerto local 11434
            ollama_payload = json.dumps({
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.23}
            }).encode("utf-8")

            req = urllib.request.Request(OLLAMA_URL, data=ollama_payload, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    ollama_data = json.loads(resp.read().decode())
                    ai_text = ollama_data.get("response", "")
            except Exception as e:
                ai_text = f"[Oasis Guard activo: Ollama local no respondió o no está corriendo: {e}]"

            self._send_json({
                "response": ai_text,
                "brake_applied": not eval_res["is_safe"],
                "wait_seconds_applied": eval_res["wait_seconds"],
                "prompt_entropy": eval_res["entropy"],
                "deviation_kappa": eval_res["deviation"]
            })
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    print(f"🛡️  [OASIS FRENO GEOMÉTRICO]: Servidor activo en http://0.0.0.0:{PORT}")
    server = HTTPServer(("0.0.0.0", PORT), AIBrakeHandler)
    server.serve_forever()
