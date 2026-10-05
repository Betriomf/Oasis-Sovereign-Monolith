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
MASTER_KEY = os.environ.get("OASIS_MASTER_KEY", "OASIS-SOVEREIGN-MARIANO-2026")

# Parámetros Chaumianos (e, N) y d
RSA_E = 17
RSA_N = 3233
RSA_D = 2753
SPENT_NULLIFIERS = set()

AUTH_KEYS = {
    MASTER_KEY: {"quota": float("inf"), "owner": "sovereign_root"}
}

VORTEX_CACHE = {}
MAX_CACHE_ENTRIES = 25000
BATCH_QUEUE = []
QUEUE_LOCK = threading.Lock()

def supabase_batch_worker():
    while True:
        time.sleep(2.0)
        batch = []
        with QUEUE_LOCK:
            if BATCH_QUEUE:
                batch = BATCH_QUEUE[:50]
                del BATCH_QUEUE[:len(batch)]
        if batch:
            try:
                url = f"{SUPABASE_URL}/rest/v1/game_fluid_states"
                headers = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                }
                req = urllib.request.Request(url, data=json.dumps(batch).encode("utf-8"), headers=headers, method="POST")
                urllib.request.urlopen(req, timeout=5)
            except Exception:
                pass

threading.Thread(target=supabase_batch_worker, daemon=True).start()

def compute_game_vortex(x, y, z, t, helicity=1.0):
    cache_key = hashlib.sha256(f"{x:.4f}:{y:.4f}:{z:.4f}:{t:.4f}:{helicity:.4f}".encode("utf-8")).hexdigest()
    if cache_key in VORTEX_CACHE:
        return VORTEX_CACHE[cache_key], True, cache_key

    kappa = math.log(10)
    r = math.sqrt(x*x + y*y) + 1e-6
    decay = math.exp(-0.1 * t)
    enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))

    u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
    u_z = round( math.cos(kappa * r) * decay, 4)
    res = ([u_x, u_y, u_z], round(enstrophy_limit, 4))
    
    if len(VORTEX_CACHE) < MAX_CACHE_ENTRIES:
        VORTEX_CACHE[cache_key] = res
    return res, False, cache_key

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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key, x-oasis-ecash")
        self.end_headers()

    def _authenticate(self):
        # 1. Vía Token Chaumiano eCash (Privacidad Absoluta)
        ecash_hdr = self.headers.get("x-oasis-ecash")
        if ecash_hdr and ":" in ecash_hdr:
            try:
                s_m, s_s = ecash_hdr.split(":")
                serial_m = int(s_m)
                signature_s = int(s_s)
                
                if pow(signature_s, RSA_E, RSA_N) == (serial_m % RSA_N):
                    nullifier = hashlib.sha256(str(serial_m).encode("utf-8")).hexdigest()
                    if nullifier not in SPENT_NULLIFIERS:
                        SPENT_NULLIFIERS.add(nullifier)
                        return True, {"owner": "chaumian_anonymous", "quota": "ecash_spent"}
                    return False, "Token eCash ya utilizado (Intento de doble gasto rechazado)", 402
            except Exception:
                return False, "Cabecera x-oasis-ecash corrupta", 400

        # 2. Vía API Key Convencional
        api_key = self.headers.get("x-api-key")
        if not api_key:
            return False, f"Pago requerido. Proporciona 'x-api-key' o un token eCash en 'x-oasis-ecash'. Wallet: {AKASH_WALLET}", 402

        if api_key not in AUTH_KEYS:
            return False, "Clave API inválida", 403

        entry = AUTH_KEYS[api_key]
        if entry["quota"] <= 0:
            return False, f"Cuota agotada. Envía 1 AKT/USDC a {AKASH_WALLET}", 402

        if entry["quota"] != float("inf"):
            entry["quota"] -= 1

        return True, entry, 200

    def do_GET(self):
        if self.path in ("/", "", "/telemetry", "/healthz"):
            self._send_json({
                "status": "ONLINE",
                "system": "Oasis Sovereign Monolith",
                "mint_public_key": {"e": RSA_E, "N": RSA_N},
                "wallet_beneficiary": AKASH_WALLET,
                "cached_vortices": len(VORTEX_CACHE)
            })
        elif self.path == "/status":
            self._send_json({
                "network": "Cosmos IBC / Akash Network",
                "deposit_address": AKASH_WALLET,
                "services": [
                    {"endpoint": "/v1/shield/entropy-score", "price": "0.005 USDC"},
                    {"endpoint": "/v1/game/vortex", "price": "0.01 USDC"}
                ]
            })
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        # Emisión de Firma Ciega Chaumiana
        if self.path == "/v1/ecash/blind-sign":
            blinded_m = body.get("blinded_message")
            if not blinded_m:
                self._send_json({"error": "blinded_message requerido"}, status=400)
                return
            blind_sig = pow(int(blinded_m), RSA_D, RSA_N)
            self._send_json({
                "blind_signature": blind_sig,
                "mint_e": RSA_E,
                "mint_N": RSA_N,
                "status": "FIRMADO_A_CIEGAS"
            })
            return

        # Registro de Clientes
        if self.path == "/v1/auth/register":
            new_key = f"OASIS-KEY-{uuid.uuid4().hex}"
            AUTH_KEYS[new_key] = {"quota": 1000, "owner": body.get("client_id", "external_dev")}
            self._send_json({
                "api_key": new_key,
                "free_quota": 1000,
                "instructions": "Usa x-api-key en las cabeceras.",
                "wallet": AKASH_WALLET
            }, status=201)
            return

        # Validación del acceso comercial
        auth_ok, auth_res, code = self._authenticate() if len(self._authenticate()) == 3 else (self._authenticate()[0], self._authenticate()[1], 200)
        if not auth_ok:
            self._send_json({"error": "PAGO_REQUERIDO", "motivo": auth_res}, status=code)
            return

        if self.path == "/v1/shield/entropy-score":
            intervals = body.get("intervals_ms", [])
            mean = sum(intervals) / (len(intervals) + 1e-6)
            self._send_json({
                "target_id": body.get("target_id", "anon"),
                "is_bot": len(intervals) >= 3 and mean < 60.0,
                "entropy_status": "EVALUADO_CON_EXITO",
                "auth": auth_res.get("owner")
            })
        elif self.path == "/v1/game/vortex":
            x, y, z, t = float(body.get("x", 1.0)), float(body.get("y", 0.5)), float(body.get("z", 2.0)), float(body.get("t", 0.1))
            (vel, enstrophy), is_cached, cache_h = compute_game_vortex(x, y, z, t)
            with QUEUE_LOCK:
                BATCH_QUEUE.append({"session_id": body.get("session_id", "anon"), "helicity": 1.0, "enstrophy_bound": enstrophy, "state_vector": vel})
            self._send_json({
                "velocity": vel,
                "enstrophy_bound": enstrophy,
                "cache_hit": is_cached,
                "auth": auth_res.get("owner")
            })
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), OasisCloudHandler)
    server.serve_forever()
