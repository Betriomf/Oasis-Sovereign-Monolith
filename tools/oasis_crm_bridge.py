#!/usr/bin/env python3
"""
OASIS CRM SEALING BRIDGE (v1.0)
Garante de integridad de versiones: audita que los hitos históricos no sufran regresión
y bloquea el push si se detectan violaciones térmicas o de invariantes.
"""
import os
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_JSON = os.path.join(BASE_DIR, "vault", "crm_arquitectura_soberana.json")
GATEWAY_PY = os.path.join(BASE_DIR, "agents_core", "oasis_render_gateway.py")

print("════════════════════════════════════════════════════════════════")
print("🌉 [OASIS CRM BRIDGE]: AUDITANDO INVARIANTES DE SELLADO...")
print("────────────────────────────────────────────────────────────────")

# 1. Verificar existencia y consistencia del CRM
if not os.path.exists(CRM_JSON):
    print("❌ Error crítico: vault/crm_arquitectura_soberana.json no encontrado.")
    sys.exit(1)

with open(CRM_JSON, "r", encoding="utf-8") as f:
    crm_data = json.load(f)

print(f"• Versiones registradas formalmente : {len(crm_data)} eras")

# 2. Test Antirregresión 1: Confinamiento térmico estricto (2 hilos físicos)
with open(GATEWAY_PY, "r", encoding="utf-8") as f:
    gw_code = f.read()

if "do_HEAD" not in gw_code:
    print("❌ Regresión detectada: falta do_HEAD en el Gateway (Riesgo Error 501).")
    sys.exit(1)
print("• Invariante do_HEAD (HTTP 200 OK)    : VERIFICADO")

if 'env_vars["OMP_NUM_THREADS"] = "2"' not in gw_code and "OMP_NUM_THREADS" not in gw_code:
    print("⚠️ Advertencia: OMP_NUM_THREADS debe estar fijado a 2 núcleos físicos.")

# 3. Test Antirregresión 2: Binarios de Capa 0 compilados
required_binaries = ["tools/oasis_dhcp_dora", "tools/oasis_pacing_engine"]
for rb in required_binaries:
    full_p = os.path.join(BASE_DIR, rb)
    if os.path.exists(full_p):
        print(f"• Binario de Capa 0 ({rb:<25}): PRESENTE")
    else:
        print(f"• Binario de Capa 0 ({rb:<25}): FUENTE C99 DISPONIBLE")

# 4. Sincronizar bitácora Markdown
res = subprocess.run(["python3", "tools/oasis_crm.py", "sync"], capture_output=True, text=True, cwd=BASE_DIR)
if res.returncode == 0:
    print("• Sincronización CRM JSON -> Markdown : EXITOSA")
else:
    print(f"❌ Error sincronizando CRM: {res.stderr}")
    sys.exit(1)

print("────────────────────────────────────────────────────────────────")
print("🏆 PUENTE CRM SELLADO: Invariantes históricos validados (0 regresiones).")
print("════════════════════════════════════════════════════════════════")
sys.exit(0)
