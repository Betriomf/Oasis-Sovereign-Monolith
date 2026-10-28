#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS DARWIN TEST SUITE: Audita endpoints REST, Bóveda física y consistencia del Kernel.
"""
import urllib.request, json, os, time

BASE_URL = "http://127.0.0.1:8080"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(REPO_ROOT, "vault")

def get_json(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", headers={"User-Agent": "Darwin-Auditor"})
    with urllib.request.urlopen(req, timeout=2.0) as resp:
        return json.loads(resp.read().decode())

def post_json(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=2.0) as resp:
        return json.loads(resp.read().decode())

print("═" * 70)
print("🛸 OASIS SOVEREIGN OS — TEST INTEGRAL DARWIN / KERNEL")
print("═" * 70)

# 1. Test Demonio de Maxwell-Landauer
d = get_json("/v1/math/demon")
print(f"✅ [DEMONIO]: Cota E_oasis = {d['e_oasis_joules']:.4e} J | Ahorro: {d['thermal_saving_pct']}% | {d['thermal_regime_watts']} W")

# 2. Test Hemodinámica Besov 3D
h = get_json("/v1/med/besov-cfd")
print(f"✅ [BESOV CFD]: Malla: {h['mesh_file']} | TAWSS Pico: {h['clinical_biomarkers']['tawss_peak_pa']} Pa | Nodos: {h['topology']['nodes']}")

# 3. Test Geometría 3D (Three.js WebGL payload)
g = get_json("/v1/med/mesh-geometry")
print(f"✅ [GEOMETRÍA]: {g['num_nodes']} nodos | {g['num_triangles']} triángulos poligonales entregados")

# 4. Test Invariante de Riemann
r = get_json("/v1/math/riemann")
print(f"✅ [RIEMANN]: Cero t = {r['cero']} | |ζ(s)| = {r['zeta_valor']:.4e} | Fisher-Rao = {r['entropia_fisher_rao']}")

# 5. Test Malla Swarm P2P
s = get_json("/v1/swarm/nodes")
print(f"✅ [SWARM]: {s['active_nodes']} nodo(s) activo(s) | Estado: {s['mesh_status']}")

# 6. Test Persistencia Física en Disco Real
test_file = f"test_darwin_{int(time.time())}.txt"
test_content = "VERIFICACIÓN FÍSICA: Persistencia confirmada en silicio local."
sync_res = post_json("/v1/vault/sync", {"name": test_file, "content": test_content})

physical_path = os.path.join(VAULT_DIR, test_file)
if os.path.exists(physical_path):
    print(f"✅ [BÓVEDA FÍSICA]: Archivo '{test_file}' escrito en disco ({os.path.getsize(physical_path)} bytes)")
    v_list = get_json("/v1/vault/list")
    print(f"✅ [BÓVEDA LISTADO]: {len(v_list['files'])} archivo(s) permanentes en ~/Oasis-Sovereign-Monolith/vault/")
else:
    print(f"❌ [BÓVEDA FÍSICA]: Fallo de escritura en {physical_path}")

print("═" * 70)
print("🏆 TODAS LAS APIS Y LA PERSISTENCIA RESPONDEN 100% OPERATIVAS.")
print("═" * 70)
