#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — MOTOR DE DEPÓSITO CIENTÍFICO EN ZENODO (CERN)
Publica y reserva DOIs inmutables para el CRM, la física de Capa 0 y el código.
"""
import os
import sys
import json
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")

ZENODO_TOKEN = os.getenv("ZENODO_TOKEN", "").strip()
ZENODO_API_URL = "https://zenodo.org/api/deposit/depositions"

def run_zenodo_deposit(existing_id=None):
    print("════════════════════════════════════════════════════════════════")
    print("🏛️ [ZENODO CERN DEPÓSITO]: INICIANDO REGISTRO FORMAL...")
    print("────────────────────────────────────────────────────────────────")

    if not ZENODO_TOKEN:
        print("❌ Error: Variable ZENODO_TOKEN no definida en el entorno.")
        print("Ejecuta antes: export ZENODO_TOKEN='tu_token_aqui'")
        sys.exit(1)

    headers_json = {
        "Authorization": f"Bearer {ZENODO_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 1. Obtener o crear el registro (Deposition)
    deposition = None
    if existing_id:
        print(f"🔄 Reutilizando borrador existente ID: {existing_id}...")
        try:
            req = urllib.request.Request(f"{ZENODO_API_URL}/{existing_id}", headers=headers_json, method="GET")
            with urllib.request.urlopen(req, timeout=15) as resp:
                deposition = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"⚠️ No se pudo recuperar borrador {existing_id}: {e}. Creando nuevo...")

    if not deposition:
        req = urllib.request.Request(ZENODO_API_URL, data=json.dumps({}).encode("utf-8"), headers=headers_json, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                deposition = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"❌ Error HTTP {e.code}: {e.read().decode('utf-8')}")
            sys.exit(1)

    deposition_id = deposition["id"]
    bucket_url = deposition.get("links", {}).get("bucket")
    doi_reserved = deposition.get("metadata", {}).get("prereserve_doi", {}).get("doi", f"10.5281/zenodo.{deposition_id}")

    print(f"• ID de Depósito Zenodo : {deposition_id}")
    print(f"• DOI Prereservado       : {doi_reserved}")
    print(f"• Bucket de Subida      : {bucket_url}")

    # 2. Archivos a subir
    files_to_upload = [
        ("crm_arquitectura_soberana.json", os.path.join(VAULT_DIR, "crm_arquitectura_soberana.json")),
        ("bitacora_arquitectura_crm.md", os.path.join(VAULT_DIR, "bitacora_arquitectura_crm.md")),
        ("oasis_tech_index.json", os.path.join(VAULT_DIR, "oasis_tech_index.json")),
        ("bitcoin_ots_manifest.json", os.path.join(VAULT_DIR, "bitcoin_ots_manifest.json")),
        ("AUTHORS.md", os.path.join(BASE_DIR, "AUTHORS.md")),
        ("LICENSE", os.path.join(BASE_DIR, "LICENSE"))
    ]

    print("\n📤 Subiendo archivos de Capa 0 al almacenamiento del CERN...")
    for filename, filepath in files_to_upload:
        if os.path.exists(filepath):
            with open(filepath, "rb") as fp:
                file_data = fp.read()
            upload_url = f"{bucket_url}/{filename}"
            
            # Cabecera application/octet-stream obligatoria para evitar error 415
            upload_req = urllib.request.Request(
                upload_url,
                data=file_data,
                headers={
                    "Authorization": f"Bearer {ZENODO_TOKEN}",
                    "Content-Type": "application/octet-stream"
                },
                method="PUT"
            )
            with urllib.request.urlopen(upload_req, timeout=30) as up_resp:
                if up_resp.status in [200, 201]:
                    print(f"  ✅ Subido: {filename} ({len(file_data)/1024:.1f} KB)")
        else:
            print(f"  ⚠️ Archivo no encontrado: {filepath}")

    # 3. Metadatos de Autoría y Licencia
    metadata_payload = {
        "metadata": {
            "title": "Oasis Sovereign OS: Architecture CRM, Cold Silicon Invariants (<= 2.58 W), and Formal Lean 4 Verification",
            "upload_type": "software",
            "description": (
                "Technical genealogy, architectural invariants, and formal verification records of Oasis Sovereign OS (v1.0 to v20.0). "
                "Integrates Navier-Stokes analytical enstrophy bounds (kappa = ln 10, Pilar 378), cold silicon passive dissipation ceilings, "
                "C99 SIMD kernels, Lean 4 headless verification, and Zero-Knowledge OPFS storage. "
                "Conceived, engineered, and mathematically verified by Mariano Panzano Caballé."
            ),
            "creators": [
                {
                    "name": "Panzano Caballé, Mariano",
                    "affiliation": "Oasis Sovereign Monolith Core"
                }
            ],
            "access_right": "open",
            "license": "AGPL-3.0-or-later",
            "keywords": [
                "Sovereign OS",
                "Cold Silicon",
                "Navier-Stokes",
                "Lean 4",
                "C99 SIMD",
                "Golden Pacing",
                "Zero-Knowledge",
                "Architecture CRM"
            ]
        }
    }

    # 4. Actualizar metadatos
    meta_url = f"{ZENODO_API_URL}/{deposition_id}"
    meta_req = urllib.request.Request(
        meta_url,
        data=json.dumps(metadata_payload).encode("utf-8"),
        headers=headers_json,
        method="PUT"
    )
    with urllib.request.urlopen(meta_req, timeout=15) as meta_resp:
        updated_dep = json.loads(meta_resp.read().decode("utf-8"))
        print("\n✅ Metadatos formales asociados con éxito.")

    # 5. Guardar recibo en la Bóveda
    receipt_path = os.path.join(VAULT_DIR, "zenodo_deposition_receipt.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(updated_dep, f, indent=2, ensure_ascii=False)

    print("────────────────────────────────────────────────────────────────")
    print(f"🎉 DEPÓSITO COMPLETADO EN MODO BORRADOR")
    print(f"• URL en Zenodo             : https://zenodo.org/deposit/{deposition_id}")
    print(f"• Recibo generado           : {receipt_path}")
    print(f"• DOI Prereservado          : {doi_reserved}")
    print("════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    target_id = sys.argv[1] if len(sys.argv) > 1 else "24137568"
    run_zenodo_deposit(target_id)
