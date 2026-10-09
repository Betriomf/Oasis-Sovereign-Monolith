#!/usr/bin/env python3
"""
OASIS PRE-PUSH VERIFICATION SUITE v1.0
Comprueba que los comandos heredados y endpoints de Capa 0 respondan HTTP 200/OK.
"""
import sys
import json
import urllib.request
import time

GATEWAY_URL = "https://oasis-sovereign-gateway.onrender.com"

TEST_ENDPOINTS = [
    ("/", "GET", None),
    ("/terminal", "GET", None),
    ("/v1/agent/status", "GET", None),
    ("/v1/reports/latest", "GET", None),
    ("/v1/game/vortex", "POST", {"x": 1.5, "y": 0.8, "z": 2.0, "elliptic": True})
]

def run_suite():
    print("=" * 60)
    print("🧪 EJECUTANDO SUITE DE COMPROBACIÓN PRE-PUSH OASIS")
    print("=" * 60)
    all_ok = True

    for path, method, payload in TEST_ENDPOINTS:
        url = f"{GATEWAY_URL}{path}"
        t0 = time.time()
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-oasis-caps": "0x0007"
                },
                method=method
            )
            data = json.dumps(payload).encode() if payload else None
            with urllib.request.urlopen(req, data=data, timeout=6) as resp:
                elapsed = round((time.time() - t0) * 1000, 1)
                st = resp.status
                if st in (200, 204):
                    print(f"  ✅ [PASS] {method} {path} (HTTP {st}) - {elapsed} ms")
                else:
                    print(f"  ⚠️ [WARN] {method} {path} (HTTP {st}) - {elapsed} ms")
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 1)
            print(f"  ❌ [FAIL] {method} {path} - Error: {e} ({elapsed} ms)")
            all_ok = False

    print("=" * 60)
    if all_ok:
        print("🏁 RESULTADO: Todos los canales responden correctamente. Seguro para commit.")
        sys.exit(0)
    else:
        print("🚨 RESULTADO: Fallos detectados en el Gateway. Revisa la conexión.")
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
