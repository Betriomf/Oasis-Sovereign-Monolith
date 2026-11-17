#!/usr/bin/env python3
"""
[FASE 8 — SELLO DE LA VERDAD]: PUBLICADOR AUTOMÁTICO EN ZENODO VÍA API REST
"""
import json
import os
import ssl
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
API_BASE = "https://zenodo.org/api/deposit/depositions"
SSL_CTX = ssl._create_unverified_context()

FILES_TO_DEPOSIT = [
    "papers/paper_a_pilar378_lincos_lean4_zenodo_clean.tex",
    "papers/paper_b_yang_mills_spectral_bounds_zenodo_clean.tex",
    "formal_proofs/YangMills_SpectralGap.lean",
    "formal_proofs/YangMills_Wilson_FisherRao.lean",
    "formal_proofs/YangMills_OsterwalderSchrader_Fase5.lean",
    "tools/ym_su2_mc_c99.c",
]

def api_request(url: str, token: str, method: str = "GET", data: bytes | None = None, content_type: str = "application/json") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
        "User-Agent": "OasisZenodoPublisher/21.7"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

def main():
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        print("❌ Falta ZENODO_TOKEN.")
        sys.exit(1)

    publish_now = "--publish" in sys.argv
    print("🌐 [FASE 8 — ZENODO]: Creando depósito científico en Zenodo...")
    dep = api_request(API_BASE, token, method="POST", data=b"{}")
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    prereserved_doi = dep.get("metadata", {}).get("prereserved_doi", {}).get("doi", "pendiente")
    print(f"📦 Depósito creado: ID={dep_id} | DOI pre-reservado: {prereserved_doi}")

    for rel in FILES_TO_DEPOSIT:
        fpath = BASE_DIR / rel
        if not fpath.exists():
            print(f"  ⚠️ Omitiendo: {rel}")
            continue
        upload_url = f"{bucket_url}/{fpath.name}"
        api_request(upload_url, token, method="PUT", data=fpath.read_bytes(), content_type="application/octet-stream")
        print(f"  ✅ Subido a Zenodo: {fpath.name} ({fpath.stat().st_size} bytes)")

    metadata = {
        "metadata": {
            "title": "Oasis Sovereign Monolith: Machine-Checked Lean 4 Spectral Gap Bounds in Discretized Yang-Mills Theory and Decadic Enstrophy Confinement",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": (
                "Machine-checked formal verification suite in Lean 4 (sorry = 0) and C99 cold-silicon SU(2) lattice simulation "
                "establishing: (1) Decadic Enstrophy Attractor (kappa = ln 10) and LINCOS symbolic compression (Paper A); "
                "and (2) Effective scalar 0++ glueball spectral gap bounds, Wilson lattice action non-negativity, "
                "Fisher-Rao informational filtering, and Osterwalder-Schrader reflection positivity in regularized SU(N) Yang-Mills theory (Paper B)."
            ),
            "creators": [{"name": "Panzano Caballé, Mariano", "affiliation": "Oasis Sovereign Architecture Research, Barcelona"}],
            "keywords": ["Lean 4", "Formal Verification", "Yang-Mills Theory", "Spectral Gap", "Navier-Stokes", "Osterwalder-Schrader", "Lattice Gauge Theory"],
            "license": "cc-by-4.0",
            "related_identifiers": [
                {"identifier": "https://github.com/Betriomf/Oasis-Sovereign-Monolith", "relation": "isSupplementedBy", "scheme": "url"}
            ]
        }
    }
    api_request(f"{API_BASE}/{dep_id}", token, method="PUT", data=json.dumps(metadata).encode("utf-8"))
    print("📝 Metadatos registrados en Zenodo.")

    if publish_now:
        pub = api_request(f"{API_BASE}/{dep_id}/actions/publish", token, method="POST", data=b"")
        final_doi = pub.get("doi", prereserved_doi)
        print(f"🏆 ¡PUBLICADO EN ZENODO! DOI OFICIAL PERMANENTE: https://doi.org/{final_doi}")
    else:
        print(f"🔒 Borrador listo en: https://zenodo.org/uploads/{dep_id}")

if __name__ == "__main__":
    main()
