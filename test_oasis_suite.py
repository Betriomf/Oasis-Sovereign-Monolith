#!/usr/bin/env python3
import time
import json
import urllib.request

GATEWAY_URL = "https://oasis-sovereign-gateway.onrender.com"

def run_test(url, method="GET", payload=None):
    t0 = time.time()
    try:
        data = json.dumps(payload).encode() if payload else None
        headers = {"Content-Type": "application/json"} if payload else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=8) as resp:
            ms = round((time.time() - t0) * 1000, 1)
            return True, resp.status, ms, json.loads(resp.read().decode())
    except Exception as e:
        return False, str(e), round((time.time() - t0) * 1000, 1), {}

print("\n🧪 [AUDITORÍA DE ENDPOINTS CAPA 0]")
# 1. BKM Audit (Paper 2)
ok, st, ms, res = run_test(f"{GATEWAY_URL}/v1/math/bkm-audit")
print(f"  • Beale-Kato-Majda : {'✅ PASS' if ok else '❌ FAIL'} ({ms} ms) -> {res.get('status')}")

# 2. Besov Shield (Paper 3)
ok, st, ms, res = run_test(f"{GATEWAY_URL}/v1/shield/status")
print(f"  • Besov Shield     : {'✅ PASS' if ok else '❌ FAIL'} ({ms} ms) -> {res.get('power_budget')}")

# 3. Navier-Stokes Vortex (Paper 1)
ok, st, ms, res = run_test(f"{GATEWAY_URL}/v1/game/vortex", "POST", {"x": 1.5, "y": 0.8, "z": 2.0, "elliptic": True})
print(f"  • Navier-Stokes    : {'✅ PASS' if ok else '❌ FAIL'} ({ms} ms) -> Cota: {res.get('enstrophy_bound')}")
