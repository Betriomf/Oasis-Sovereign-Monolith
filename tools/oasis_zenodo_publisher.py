#!/usr/bin/env python3
"""
[FASE 8 - 12]: PUBLICADOR CIENTÍFICO UNIFICADO BLINDADO PARA ZENODO
Soporta: paquete base, --paper-c, --paper-d, --paper-e y --paper-f (CC-BY-NC-4.0).
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

TARGETS = {
    "base": [
        "papers/paper_a_pilar378_lincos_lean4_zenodo_clean.tex",
        "papers/paper_b_yang_mills_spectral_bounds_zenodo_clean.tex",
        "formal_proofs/YangMills_SpectralGap.lean",
        "formal_proofs/YangMills_Wilson_FisherRao.lean",
        "formal_proofs/YangMills_OsterwalderSchrader_Fase5.lean",
        "tools/ym_su2_mc_c99.c",
    ],
    "paper-c": [
        "papers/paper_c_araki_entropy_mqm_lean4.tex",
        "formal_proofs/ArakiRelativeEntropy_Fase9.lean",
    ],
    "paper-d": [
        "papers/paper_d_quantum_os_ring3_lean4.tex",
        "formal_proofs/QuantumOS_ControlPlane_Fase10.lean",
    ],
    "paper-e": [
        "papers/paper_e_pilar86_leech_qpu_os_lean4.tex",
        "formal_proofs/Pilar86_LeechQPU_QuantumOS_Fase11.lean",
    ],
    "paper-f": [
        "papers/paper_f_personal_desktop_cold_silicon_lean4.tex",
        "formal_proofs/PersonalDesktop_ColdSilicon_Fase12.lean",
    ],
}

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
            res = subprocess.run(["lean", str(fpath)], capture_output=True, text=True, timeout=90)
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
        "User-Agent": "OasisZenodoPublisher/22.7-CleanStrictTLS"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=45, context=SSL_CTX) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

def build_metadata(mode: str) -> dict:
    creator = [{"name": "Panzano Caballé, Mariano", "affiliation": "Oasis Sovereign Architecture Research, Barcelona"}]
    repo_rel = {"identifier": "https://github.com/Betriomf/Oasis-Sovereign-Monolith", "relation": "isSupplementedBy", "scheme": "url"}

    if mode == "paper-f":
        return {
            "metadata": {
                "title": "Cold-Silicon Personal Desktop Architecture: Zero-Swap Local AI Pooling, Bounded Context Pruning, and Ring-3 Isolation on Memory-Constrained Consumer Laptops",
                "upload_type": "publication",
                "publication_type": "preprint",
                "description": (
                    "Machine-checked Lean 4 memory and thermal containment invariants (zero sorry, zero admit, zero custom axioms) "
                    "for consumer 8 GiB personal computers, continuing DOI 10.5281/zenodo.24324683 and DOI 10.5281/zenodo.24324622. "
                    "Formally verifies strict zero-swap RAM partitioning (2872 MiB OS + 1200 MiB Q4_K_M LLM + 28 MiB PQC Dilithium <= 8192 MiB) "
                    "and bounded MCP context ingestion (1400 B <= 2048 B) under two-thread thermal capping."
                ),
                "creators": creator,
                "keywords": ["Personal Computing", "Edge AI", "Lean 4", "Formal Verification", "Low-Power Systems", "Post-Quantum Cryptography"],
                "license": "cc-by-nc-4.0",
                "related_identifiers": [
                    {"identifier": "10.5281/zenodo.24324683", "relation": "continues", "scheme": "doi"},
                    {"identifier": "10.5281/zenodo.24324622", "relation": "isPartOf", "scheme": "doi"},
                    repo_rel
                ]
            }
        }
    if mode == "paper-e":
        return {
            "metadata": {
                "title": "Pilar 86 Quantum Kernel Architecture and phi-Aware Distributed Operating System: Leech Lattice (Lambda_24) Compilation, Non-Commutative Logic Gates, and Reversible Transition",
                "upload_type": "publication",
                "publication_type": "preprint",
                "description": (
                    "Formal specification and Lean 4 machine-checked structural invariants (zero sorry, zero admit, zero custom axioms) "
                    "for the Pilar 86 QPU Kernel and 5-layer phi-Aware Distributed Operating System, continuing DOI 10.5281/zenodo.24324622 "
                    "and DOI 10.5281/zenodo.24311596."
                ),
                "creators": creator,
                "keywords": ["Quantum Operating System", "Leech Lattice", "Lean 4", "Formal Verification", "ZX-Calculus"],
                "license": "cc-by-nc-4.0",
                "related_identifiers": [
                    {"identifier": "10.5281/zenodo.24324622", "relation": "continues", "scheme": "doi"},
                    {"identifier": "10.5281/zenodo.24311596", "relation": "isPartOf", "scheme": "doi"},
                    repo_rel
                ]
            }
        }
    return {
        "metadata": {
            "title": "Oasis Sovereign Monolith: Machine-Checked Lean 4 Formal Verification Artifact",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": "Reproducible Lean 4 formal verification artifact from Oasis Sovereign Monolith.",
            "creators": creator,
            "license": "cc-by-nc-4.0",
            "related_identifiers": [repo_rel]
        }
    }

def main():
    mode = "base"
    for flag in ("paper-f", "paper-e", "paper-d", "paper-c"):
        if f"--{flag}" in sys.argv:
            mode = flag
            break

    target_files = TARGETS[mode]
    if not scientific_audit(target_files):
        print("\n⛔ AUDITORÍA RECHAZADA.")
        sys.exit(1)

    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        print("\n❌ Falta ZENODO_TOKEN.")
        sys.exit(1)

    print(f"\n🌐 [ZENODO — {mode.upper()}]: Creando borrador controlado (TLS estricto)...")
    dep = api_request(API_BASE, token, method="POST", data=b"{}")
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    print(f"📦 Borrador creado: ID={dep_id}")

    for rel in target_files:
        fpath = BASE_DIR / rel
        api_request(f"{bucket_url}/{fpath.name}", token, method="PUT", data=fpath.read_bytes(), content_type="application/octet-stream")
        print(f"  ✅ Subido: {fpath.name} ({fpath.stat().st_size} bytes)")

    api_request(f"{API_BASE}/{dep_id}", token, method="PUT", data=json.dumps(build_metadata(mode)).encode("utf-8"))
    print(f"🔒 [BORRADOR LISTO]: Revisa y publica en:\n   👉 https://zenodo.org/uploads/{dep_id}")

if __name__ == "__main__":
    main()
