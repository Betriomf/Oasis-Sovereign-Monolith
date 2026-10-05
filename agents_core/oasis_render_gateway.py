#!/usr/bin/env python3
import os
import json
import math
import time
import uuid
import hashlib
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"

# Clave Maestra Soberana: Acceso ilimitado garantizado
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

# Almacén de Claves: { key: { "quota": int/float, "owner": str } }
AUTH_KEYS = {
    MASTER_KEY: {"quota": float("inf"), "owner": "sovereign_root"}
}

VORTEX_CACHE = {}
MAX_CACHE_ENTRIES = 25000
BATCH_QUEUE = []
QUEUE_LOCK = threading.Lock()
BATCH_MAX_SIZE = 50
BATCH_INTERVAL_SEC = 2.0

def supabase_batch_worker():
    while True:
        time.sleep(BATCH_INTERVAL_SEC)
        batch_to_send = []
        with QUEUE_LOCK:
            if BATCH_QUEUE:
                batch_to_send = BATCH_QUEUE[:BATCH_MAX_SIZE]
                del BATCH_QUEUE[:len(batch_to_send)]

        if batch_to_send:
            try:
                url = f"{SUPABASE_URL}/rest/v1/game_fluid_states"
                headers = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                }
                payload = json.dumps(batch_to_send).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    pass
            except Exception:
                pass

worker_thread = threading.Thread(target=supabase_batch_worker, daemon=True)
worker_thread.start()

def evaluate_intervals_entropy(intervals):
    if not intervals or len(intervals) < 3:
        return 50.0, "INSUFFICIENT_DATA", 0.0, 0.0
    intervals_sec = [x / 1000.0 if x > 20.0 else x for x in intervals]
    mean = sum(intervals_sec) / len(intervals_sec)
    variance = sum((x - mean) ** 2 for x in intervals_sec) / len(intervals_sec)
    std_dev = math.sqrt(variance)
    cv = std_dev / (mean + 1e-6)
    entropy_score = min(100.0, max(0.0, cv * 75.0))

    if entropy_score < 15.0 or (mean < 0.15 and std_dev < 0.02):
        verdict = "BOT_SYNTHETIC"
    elif entropy_score < 40.0:
        verdict = "SUSPICIOUS_AUTOMATION"
    else:
        verdict = "ORGANIC_HUMAN"
    return round(entropy_score, 2), verdict, round(mean, 4), round(std_dev, 4)

def compute_game_vortex(x, y, z, t, helicity=1.0):
    cache_key = hashlib.sha256(f"{x:.4f}:{y:.4f}:{z:.4f}:{t:.4f}:{helicity:.4f}".encode("utf-8")).hexdigest()
    if cache_key in VORTEX_CACHE:
        vel, enstrophy = VORTEX_CACHE[cache_key]
        return vel, enstrophy, True, cache_key

    kappa = math.log(10)
    r = math.sqrt(x*x + y*y) + 1e-6
    decay = math.exp(-0.1 * t)
    enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))

    u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_z = round( math.cos(kappa * r) * decay, 4)
    vel = [u_x, u_y, u_z]
    enstrophy = round(enstrophy_limit, 4)

    if len(VORTEX_CACHE) < MAX_CACHE_ENTRIES:
        VORTEX_CACHE[cache_key] = (vel, enstrophy)
    return vel, enstrophy, False, cache_key

class OasisCloudHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key, x-client-time")
        self.end_headers()

    def _authenticate(self):
        """Valida x-api-key y gestiona la cuota de consumo."""
        api_key = self.headers.get("x-api-key")
        if not api_key:
            return False, "Cabecera 'x-api-key' obligatoria. Obtén una gratis en POST /v1/auth/register", 401

        if api_key not in AUTH_KEYS:
            return False, "Clave API inválida o no registrada", 403

        entry = AUTH_KEYS[api_key]
        if entry["quota"] <= 0:
            return False, f"Cuota agotada. Envía 1 USDC / AKT a {AKASH_WALLET} para recargar saldo.", 402

        # Descontar crédito a usuarios regulares; la clave maestra es infinita
        if entry["quota"] != float("inf"):
            entry["quota"] -= 1

        return True, entry, 200

    def do_GET(self):
        if self.path in ("/", ""):
            self._send_json({
                "status": "ONLINE",
                "system": "Oasis Sovereign Monolith",
                "auth_required": True,
                "free_tier": "1.000 llamadas gratis registradas en /v1/auth/register",
                "docs": "https://oasis-sovereign-gateway.onrender.com/docs",
                "wallet_beneficiary": AKASH_WALLET
            })
        elif self.path in ("/telemetry", "/healthz"):
            self._send_json({"status": "HEALTHY", "cached_vortices": len(VORTEX_CACHE), "active_keys": len(AUTH_KEYS)})
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "deposit_address": AKASH_WALLET,
                "supported_tokens": ["AKT", "USDC"]
            })
        elif self.path == "/api/navier-stokes":
            self._send_json({"theorem": "navier_stokes_helical_regularity", "formal_syntax": "Lean 4"})
        elif self.path == "/api/bkm-enstrophy":
            self._send_json({"operator": "dyadic_littlewood_paley_bound", "kappa_attractor": math.log(10), "bkm_stable": True})
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        # 1. Registro Gratuito de Nuevos Clientes (Sin autenticación previa)
        if self.path == "/v1/auth/register":
            owner = body.get("client_id", f"user_{uuid.uuid4().hex[:6]}")
            new_key = f"OASIS-KEY-{uuid.uuid4().hex}"
            AUTH_KEYS[new_key] = {"quota": 1000, "owner": owner}
            self._send_json({
                "status": "CREADA",
                "api_key": new_key,
                "free_quota": 1000,
                "instructions": "Añade 'x-api-key: TU_CLAVE' en las cabeceras HTTP de tus llamadas.",
                "recharge_wallet": AKASH_WALLET
            }, status=201)
            return

        # 2. Gatekeeper para Endpoints Comerciales
        auth_ok, auth_data, code = self._authenticate()
        if not auth_ok:
            self._send_json({"error": "AUTORIZACION_DENEGADA", "motivo": auth_data}, status=code)
            return

        if self.path == "/v1/shield/entropy-score":
            intervals = body.get("intervals_ms", [])
            target_id = body.get("target_id", "anon")
            score, verdict, mean_val, std_val = evaluate_intervals_entropy(intervals)
            self._send_json({
                "target_id": target_id,
                "entropy_score": score,
                "verdict": verdict,
                "is_bot": verdict != "ORGANIC_HUMAN",
                "remaining_quota": auth_data["quota"],
                "audit": "EVALUACION_TERMODINAMICA_ZERO_PII"
            })

        elif self.path == "/v1/game/vortex":
            session_id = body.get("session_id", "default_session")
            x = float(body.get("x", 1.0))
            y = float(body.get("y", 0.5))
            z = float(body.get("z", 2.0))
            t = float(body.get("t", 0.1))
            helicity = float(body.get("helicity", 1.0))

            vel, enstrophy, is_cached, cache_hash = compute_game_vortex(x, y, z, t, helicity)
            record = {"session_id": session_id, "helicity": helicity, "enstrophy_bound": enstrophy, "state_vector": vel}
            with QUEUE_LOCK:
                BATCH_QUEUE.append(record)

            self._send_json({
                "session_id": session_id,
                "velocity": vel,
                "enstrophy_bound": enstrophy,
                "bkm_stable": True,
                "cache_hit": is_cached,
                "remaining_quota": auth_data["quota"]
            })
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
