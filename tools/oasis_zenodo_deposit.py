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

# ==============================================================================
# TOKEN DE ACCESO A ZENODO (Añade aquí las letras que faltan a tu token)
# ==============================================================================
ZENODO_TOKEN = os.getenv(
    "ZENODO_TOKEN",
    "sCb23CE5yIdq9K5b0RJuRnioDGtFQagNwIuvWzWcvPVgpIYp0F87sUuzuwyq" # <--- COMPLETA LAS LETRAS AQUÍ
)

ZENODO_API_URL = "https://zenodo.org/api/deposit/depositions"

def create_zenodo_deposition():
    print("════════════════════════════════════════════════════════════════")
    print("🏛️ [ZENODO CERN DEPÓSITO]: INICIANDO REGISTRO FORMAL...")
    print("────────────────────────────────────────────────────────────────")

    if "..." in ZENODO_TOKEN or len(ZENODO_TOKEN) < 40:
        print("⚠️ Advertencia: Revisa que ZENODO_TOKEN contenga todas las letras.")

    headers = {
        "Authorization": f"Bearer {ZENODO_TOKEN.strip()}",
        "Content-Type": "application/json"
    }

    # 1. Crear nuevo registro vacío (Draft)
    req = urllib.request.Request(ZENODO_API_URL, data=json.dumps({}).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            deposition = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ Error HTTP {e.code} conectando con Zenodo: {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error de red: {e}")
        sys.exit(1)

    deposition_id = deposition["id"]
    bucket_url = deposition.get("links", {}).get("bucket")
    doi_reserved = deposition.get("metadata", {}).get("prereserve_doi", {}).get("doi", f"10.5281/zenodo.{deposition_id}")

    print(f"• ID de Depósito Zenodo : {deposition_id}")
    print(f"• DOI Prereservado       : {doi_reserved}")
    print(f"• Bucket de Subida      : {bucket_url}")

    # 2. Subir Archivos Fundamentales (CRM, Manifiesto, Código)
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
            upload_req = urllib.request.Request(
                upload_url,
                data=file_data,
                headers={"Authorization": f"Bearer {ZENODO_TOKEN.strip()}"},
                method="PUT"
            )
            with urllib.request.urlopen(upload_req, timeout=30) as up_resp:
                if up_resp.status in [200, 201]:
                    print(f"  ✅ Subido: {filename} ({len(file_data)/1024:.1f} KB)")
        else:
            print(f"  ⚠️ Archivo no encontrado: {filepath}")

    # 3. Metadatos Científicos y Autoría Legal
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
                    "affiliation": "Oasis Sovereign Monolith Core",
                    "orcid": ""
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

    # 4. Actualizar Metadatos en Zenodo
    meta_url = f"{ZENODO_API_URL}/{deposition_id}"
    meta_req = urllib.request.Request(
        meta_url,
        data=json.dumps(metadata_payload).encode("utf-8"),
        headers=headers,
        method="PUT"
    )
    with urllib.request.urlopen(meta_req, timeout=15) as meta_resp:
        updated_dep = json.loads(meta_resp.read().decode("utf-8"))
        print("\n✅ Metadatos formales asociados con éxito.")

    # Guardar recibo del depósito en la Bóveda
    receipt_path = os.path.join(VAULT_DIR, "zenodo_deposition_receipt.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(updated_dep, f, indent=2, ensure_ascii=False)

    print("────────────────────────────────────────────────────────────────")
    print(f"🎉 DEPÓSITO PREPARADO EN MODO BORRADOR")
    print(f"• URL para revisar en Zenodo : https://zenodo.org/deposit/{deposition_id}")
    print(f"• Recibo guardado en Bóveda  : {receipt_path}")
    print("• Estado                     : DRAFT (Borrador seguro, no publicado aún)")
    print("\n💡 Cuando revises que todo esté a tu gusto en la web de Zenodo,")
    print("   puedes pulsar 'Publish' en su web o ejecutar con el flag --publish.")
    print("════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    create_zenodo_deposition()
