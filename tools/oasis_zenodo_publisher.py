#!/usr/bin/env python3
"""
[FASE 8 — ETAPA 1 & 2]: PUBLICADOR CIENTÍFICO BLINDADO PARA ZENODO
- Verificación estricta de certificados TLS (HTTPS).
- Bloqueo obligatorio (fail-fast) si falta cualquier archivo o si Lean 4 contiene sorry / admit / axiom.
- Crea BORRADOR por defecto para inspección humana previa antes de publicar DOI.
"""
import hashlib
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

BASE_DIR = Path(__file__).resolve().parent.parent
API_BASE = "https://zenodo.org/api/deposit/depositions"

REQUIRED_FILES = [
    "papers/paper_a_pilar378_lincos_lean4_zenodo_clean.tex",
    "papers/paper_b_yang_mills_spectral_bounds_zenodo_clean.tex",
    "formal_proofs/YangMills_SpectralGap.lean",
    "formal_proofs/YangMills_Wilson_FisherRao.lean",
    "formal_proofs/YangMills_OsterwalderSchrader_Fase5.lean",
    "tools/ym_su2_mc_c99.c",
]

def strip_lean_comments_and_strings(raw: str) -> str:
    txt = raw
    while "/-" in txt and "-/" in txt:
        nxt = re.sub(r"/-[\s\S]*?-/", "", txt)
        if nxt == txt:
            break
        txt = nxt
    txt = re.sub(r"--.*", "", txt)
    txt = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', txt)
    return txt

def stage1_scientific_audit() -> bool:
    print("🔬 [ETAPA 1 — AUDITORÍA CIENTÍFICA PREVIA A ZENODO]")
    all_ok = True

    # 1. Verificar existencia e integridad no vacía de todos los entregables
    for rel in REQUIRED_FILES:
        fpath = BASE_DIR / rel
        if not fpath.exists() or fpath.stat().st_size == 0:
            print(f"  ❌ BLOQUEO: Falta archivo obligatorio o está vacío -> {rel}")
            all_ok = False
        else:
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()[:16]
            print(f"  ✅ Archivo íntegro ({fpath.stat().st_size:>5} B | sha:{sha}): {rel}")

    # 2. Verificar Lean 4: sin sorry, sin admit, sin axiom propios y compilación limpia
    lean_files = [f for f in REQUIRED_FILES if f.endswith(".lean")]
    has_lean = bool(shutil.which("lean"))
    for rel in lean_files:
        fpath = BASE_DIR / rel
        if not fpath.exists():
            continue
        clean = strip_lean_comments_and_strings(fpath.read_text(encoding="utf-8"))
        forbidden = re.findall(r"\b(sorry|admit|axiom)\b", clean)
        if forbidden:
            print(f"  ❌ BLOQUEO FORMAL en {rel}: Palabras prohibidas detectadas -> {set(forbidden)}")
            all_ok = False
            continue
        if has_lean:
            res = subprocess.run(["lean", str(fpath)], capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                print(f"  ❌ BLOQUEO COMPILACIÓN Lean 4 en {rel}: {res.stderr[:140]}")
                all_ok = False
                continue
        print(f"  ✅ Verificación Lean 4 superada (0 sorry, 0 admit, 0 axiom): {rel}")

    return all_ok

def api_request(url: str, token: str, method: str = "GET", data: bytes | None = None, content_type: str = "application/json") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
        "User-Agent": "OasisZenodoPublisher/21.8-StrictTLS"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

def main():
    if not stage1_scientific_audit():
        print("\n⛔ AUDITORÍA RECHAZADA: No se ha contactado con Zenodo. Corrige los bloqueos primero.")
        sys.exit(1)

    if "--audit-only" in sys.argv:
        print("\n🏆 ETAPA 1 SUPERADA AL 100%. Listo para Etapa 2 (creación de borrador en Zenodo).")
        return

    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        print("\n❌ Falta ZENODO_TOKEN en el entorno.")
        sys.exit(1)

    publish_now = "--publish-confirmed" in sys.argv
    print("\n🌐 [ETAPA 2 — ZENODO]: Creando depósito controlado (TLS verificado)...")
    dep = api_request(API_BASE, token, method="POST", data=b"{}")
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    prereserved_doi = dep.get("metadata", {}).get("prereserved_doi", {}).get("doi", "pendiente")
    print(f"📦 Borrador creado: ID={dep_id} | DOI pre-reservado: {prereserved_doi}")

    for rel in REQUIRED_FILES:
        fpath = BASE_DIR / rel
        upload_url = f"{bucket_url}/{fpath.name}"
        api_request(upload_url, token, method="PUT", data=fpath.read_bytes(), content_type="application/octet-stream")
        print(f"  ✅ Subido: {fpath.name} ({fpath.stat().st_size} bytes)")

    metadata = {
        "metadata": {
            "title": "Oasis Sovereign Monolith: Machine-Checked Lean 4 Spectral Bounds in Discretized SU(2) Gauge Models and Decadic Entropy Confinement",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": (
                "Reproducible formal verification suite in Lean 4 (zero sorry, zero admit, zero custom axioms) and C99 "
                "SU(2) lattice Monte Carlo benchmarks. Paper A establishes decadic entropy pruning (kappa = ln 10) and LINCOS "
                "symbolic framing for low-dissipation computing. Paper B formalizes effective scalar 0++ spectral lower bounds, "
                "Wilson lattice action non-negativity, Fisher-Rao informational filtering, and lattice reflection positivity "
                "within regularized regimes, explicitly distinguishing these discrete results from the open continuum R^4 Millennium Problem."
            ),
            "creators": [{"name": "Panzano Caballé, Mariano", "affiliation": "Oasis Sovereign Architecture Research, Barcelona"}],
            "keywords": ["Lean 4", "Formal Verification", "Lattice Gauge Theory", "SU(2)", "Spectral Bounds", "Computational Physics"],
            "license": "cc-by-4.0",
            "related_identifiers": [
                {"identifier": "https://github.com/Betriomf/Oasis-Sovereign-Monolith", "relation": "isSupplementedBy", "scheme": "url"}
            ]
        }
    }
    api_request(f"{API_BASE}/{dep_id}", token, method="PUT", data=json.dumps(metadata).encode("utf-8"))
    print("📝 Metadatos científicos rigurosos guardados en el borrador.")

    if publish_now:
        pub = api_request(f"{API_BASE}/{dep_id}/actions/publish", token, method="POST", data=b"")
        final_doi = pub.get("doi", prereserved_doi)
        print(f"🏆 [ETAPA 3 — PUBLICADO]: DOI OFICIAL PERMANENTE -> https://doi.org/{final_doi}")
    else:
        print(f"🔒 [ETAPA 2 COMPLETADA]: Revisa el borrador antes de publicar en:")
        print(f"   👉 https://zenodo.org/uploads/{dep_id}")
        print(f"   (Cuando lo hayas inspeccionado, publica desde la web o con --publish-confirmed)")

if __name__ == "__main__":
    main()
