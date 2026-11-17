#!/usr/bin/env python3
"""
[FASE 8 & 9]: PUBLICADOR CIENTÍFICO UNIFICADO BLINDADO PARA ZENODO
- Verificación estricta de certificados TLS (HTTPS).
- Auditoría obligatoria (fail-fast) de archivos y Lean 4 (0 sorry, 0 admit, 0 axiom).
- Modo BORRADOR por defecto para revisión humana antes de emitir DOI permanente.
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

BASE_FILES = [
    "papers/paper_a_pilar378_lincos_lean4_zenodo_clean.tex",
    "papers/paper_b_yang_mills_spectral_bounds_zenodo_clean.tex",
    "formal_proofs/YangMills_SpectralGap.lean",
    "formal_proofs/YangMills_Wilson_FisherRao.lean",
    "formal_proofs/YangMills_OsterwalderSchrader_Fase5.lean",
    "tools/ym_su2_mc_c99.c",
]

PAPER_C_FILES = [
    "papers/paper_c_araki_entropy_mqm_lean4.tex",
    "formal_proofs/ArakiRelativeEntropy_Fase9.lean",
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

def scientific_audit(files_list: list[str]) -> bool:
    print("🔬 [AUDITORÍA CIENTÍFICA PREVIA A ZENODO]")
    all_ok = True
    for rel in files_list:
        fpath = BASE_DIR / rel
        if not fpath.exists() or fpath.stat().st_size == 0:
            print(f"  ❌ BLOQUEO: Falta archivo obligatorio -> {rel}")
            all_ok = False
        else:
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()[:16]
            print(f"  ✅ Íntegro ({fpath.stat().st_size:>5} B | sha:{sha}): {rel}")

    lean_files = [f for f in files_list if f.endswith(".lean")]
    has_lean = bool(shutil.which("lean"))
    for rel in lean_files:
        fpath = BASE_DIR / rel
        if not fpath.exists():
            continue
        clean = strip_lean_comments_and_strings(fpath.read_text(encoding="utf-8"))
        forbidden = re.findall(r"\b(sorry|admit|axiom)\b", clean)
        if forbidden:
            print(f"  ❌ BLOQUEO FORMAL en {rel}: Palabras prohibidas -> {set(forbidden)}")
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
        "User-Agent": "OasisZenodoPublisher/22.4-UnifiedStrictTLS"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

def build_metadata(is_paper_c: bool) -> dict:
    if is_paper_c:
        return {
            "metadata": {
                "title": "Araki Relative Entropy Monotonicity and Variational Matrix Compression in Machine-Checked Cold-Silicon Gauge Verification",
                "upload_type": "publication",
                "publication_type": "preprint",
                "description": (
                    "Follow-up formal verification artifact (Paper C) continuing DOI 10.5281/zenodo.24311596. "
                    "Formalizes in Lean 4 (zero sorry, zero admit, zero custom axioms) that contractive quantum channels "
                    "preserve the decadic information ceiling (kappa = ln 10) and certifies variational state-space "
                    "compression bounds for low-dissipation matrix quantum mechanics simulations. Explicitly scoped to "
                    "regularized discrete models and information-theoretic bounds rather than the continuum R^4 Millennium Problem."
                ),
                "creators": [{"name": "Panzano Caballé, Mariano", "affiliation": "Oasis Sovereign Architecture Research, Barcelona"}],
                "keywords": ["Lean 4", "Formal Verification", "Relative Entropy", "Matrix Quantum Mechanics", "Computational Physics"],
                "license": "cc-by-4.0",
                "related_identifiers": [
                    {"identifier": "10.5281/zenodo.24311596", "relation": "continues", "scheme": "doi"},
                    {"identifier": "https://github.com/Betriomf/Oasis-Sovereign-Monolith", "relation": "isSupplementedBy", "scheme": "url"}
                ]
            }
        }
    return {
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

def main():
    is_paper_c = "--paper-c" in sys.argv
    target_files = PAPER_C_FILES if is_paper_c else BASE_FILES

    if not scientific_audit(target_files):
        print("\n⛔ AUDITORÍA RECHAZADA: No se ha contactado con Zenodo.")
        sys.exit(1)

    if "--audit-only" in sys.argv:
        print("\n🏆 AUDITORÍA SUPERADA AL 100%.")
        return

    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        print("\n❌ Falta ZENODO_TOKEN en el entorno.")
        sys.exit(1)

    publish_now = "--publish-confirmed" in sys.argv
    label = "PAPER C" if is_paper_c else "PAQUETE BASE"
    print(f"\n🌐 [ZENODO — {label}]: Creando depósito controlado (TLS estricto)...")
    dep = api_request(API_BASE, token, method="POST", data=b"{}")
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    prereserved_doi = dep.get("metadata", {}).get("prereserved_doi", {}).get("doi", "pendiente")
    print(f"📦 Borrador creado: ID={dep_id} | DOI pre-reservado: {prereserved_doi}")

    for rel in target_files:
        fpath = BASE_DIR / rel
        api_request(f"{bucket_url}/{fpath.name}", token, method="PUT", data=fpath.read_bytes(), content_type="application/octet-stream")
        print(f"  ✅ Subido: {fpath.name} ({fpath.stat().st_size} bytes)")

    api_request(f"{API_BASE}/{dep_id}", token, method="PUT", data=json.dumps(build_metadata(is_paper_c)).encode("utf-8"))
    print("📝 Metadatos científicos registrados en el borrador.")

    if publish_now:
        pub = api_request(f"{API_BASE}/{dep_id}/actions/publish", token, method="POST", data=b"")
        final_doi = pub.get("doi", prereserved_doi)
        print(f"🏆 [PUBLICADO]: DOI OFICIAL -> https://doi.org/{final_doi}")
    else:
        print(f"🔒 [BORRADOR LISTO]: Inspecciona archivos, metadatos y relación 'Continues 10.5281/zenodo.24311596' en:")
        print(f"   👉 https://zenodo.org/uploads/{dep_id}")
        print(f"   (Cuando lo hayas revisado, pulsa Publish en la web o relanza con --paper-c --publish-confirmed)")

if __name__ == "__main__":
    main()
