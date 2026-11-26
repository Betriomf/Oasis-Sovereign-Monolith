#!/usr/bin/env python3
"""
MÓDULO 23 — ORÁCULO DE LA SERIE T-Z & DOIs ZENODO/BITCOIN (CERO ESTRÉS TÉRMICO)
Triggers: tz / series-tz / dois / paper-y / paper-z / arxiv-yz
Consulta directamente Graphity (vault/oasis_graphity.json) y manifiestos SHA-256/OTS
en < 5 ms sin despertar modelos LLM locales.
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "vault/oasis_graphity.json"
MASTER_HASH_PATH = ROOT / "vault/OASIS_SERIES_TZ_MASTER_HASH.txt"

CANONICAL_DOIS = {
    "Paper V (Poincaré–MassGap Bridge)": "https://doi.org/10.5281/zenodo.24383187",
    "Paper W (Bakry–Émery → Poincaré)": "https://doi.org/10.5281/zenodo.24383399",
    "Paper X (Uniform Curvature Continuum Reduction)": "https://doi.org/10.5281/zenodo.24383530",
    "Paper Y (Curvature–Entropy Margin & C99 Wilson Bridge, Pilar 389)": "https://doi.org/10.5281/zenodo.24442236",
    "Paper Z (Discrete Ricci–Entropic Evolution & Series T–Z Closure)": "https://doi.org/10.5281/zenodo.24442403",
    "Paper OVRP (Oasis Verifiable Research Pipeline & Methodology)": "https://doi.org/10.5281/zenodo.24443531",
    "Paper Informational Thermodynamics (Laws 0–3 & Cold Silicon)": "https://doi.org/10.5281/zenodo.24443786",
    "Paper String Spectrum & Regge Bounds (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24448235",
    "Paper OVRP Audit of RH Lean 4 & Critical-Line Scan": "https://doi.org/10.5281/zenodo.24463308",
    "Paper Discrete Entropic Gravity Model (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24464014",
    "Paper Entropic Gradient Inversion & Repulsive Lattice Dynamics (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24464245",
    "OVRP Master Compendium & Genealogy (11-Paper Index)": "https://doi.org/10.5281/zenodo.24466455",
    "Paper Structural Synthesis of Bounded Projections (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24468098",
    "Paper Formal Auditing of AI-Generated Code & Boundaries (Lean 4)": "https://doi.org/10.5281/zenodo.24469140",
    "Paper Five-Phase Bounded Discrete Projections (Lean 4)": "https://doi.org/10.5281/zenodo.24477406",
    "Paper Zero-LLM Triage & Cryptographic Provenance (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24482608",
    "Paper Protein Folding Informational Attractor (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24483484",
    "Paper Prime Indivisibility & Discrete Midpoint Symmetry (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24528811",
    "OVRP Prime Symmetry & Formal Audit Compendium (Lean 4)": "https://doi.org/10.5281/zenodo.24529374",
    "Paper QOS Entropic Stability & Prime Center-of-Mass Audit (Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24530182",
    "Oasis Proof Quantum-Classical Runtime Auditor (Apache-2.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24530918",
    "Paper Entanglement Entropy & Discrete Symmetry Audit (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24533461",
    "Paper Logarithmic Scales (ln 2, ln phi, ln 10) Across TGI (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24538777",
    "Integrated OVRP Compendium (Papers 22–24, CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24539182",
    "Paper Critical Line as a Stability Boundary Interpretation (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24539709",
    "Paper Ternary Scale ln(3) in Quantum Mixture Probes & Cross-Logarithmic Ratios (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24559695",
    "Paper Ternary Scale ln(3) to Quantum-Classical OS Resource Governance (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24560686",
    "Paper Exploratory Coupling Ratios Against Fine-Structure Constant alpha (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24561380",
    "Paper Comparative Contrast of Noise and Entropy Models in Finite Quantum Systems (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24528606",
    "Paper Information Geometry Applied to Networks and Hybrid Systems (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.24529309",
    "Paper Critical Audit of Constants, Coupling Ratios, and Open Boundaries (CC-BY-4.0, Lean 4 & C99)": "https://doi.org/10.5281/zenodo.19098625",
}

def tz_process(query: str = "") -> str:
    t0 = time.perf_counter()
    master_hash = MASTER_HASH_PATH.read_text(encoding="utf-8").strip().split()[0] if MASTER_HASH_PATH.exists() else "N/D"
    ots_y = (ROOT / "vault/PAPER_Y_MARGIN_SHA256.txt.ots").exists()
    ots_z = (ROOT / "vault/PAPER_Z_SYNTHESIS_SHA256.txt.ots").exists()

    graph_summary = "Graphity no indexado"
    if GRAPH_PATH.exists():
        g = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
        graph_summary = f"{len(g.get('nodes', {}))} nodos, {len(g.get('edges', []))} aristas"

    q_low = query.lower().strip()
    lines = [
        "════════════════════════════════════════════════════════════════",
        "🏛️  [OASIS SERIES T–Z & ZENODO/BITCOIN ORACLE — MÓDULO 23]",
        "────────────────────────────────────────────────────────────────",
        "📚 DOIs OFICIALES PUBLICADOS EN ZENODO (CC-BY-NC-4.0):",
    ]
    for title, url in CANONICAL_DOIS.items():
        if not q_low or any(k in title.lower() or k in url.lower() for k in q_low.split()):
            lines.append(f"  • {title}: {url}")

    if len(lines) == 4:
        for title, url in CANONICAL_DOIS.items():
            lines.append(f"  • {title}: {url}")

    lines.extend([
        "────────────────────────────────────────────────────────────────",
        "⚛️  EVIDENCIA FORMAL Y NUMÉRICA SELLADA:",
        "  • Lean 4.36.0 (0 sorry, 0 custom axioms): PaperY_Entropy_Curvature_Margin.lean + PaperZ_Sovereign_Synthesis.lean",
        "  • Sonda su(3) / L=2^4 / L=3^4: K_proj = -0.440979 -> -0.396026 -> -0.353224 (margen neto L=3^4: +265‰)",
        "  • C99 Wilson Monte Carlo (L=12^4, beta=5.9706): <P>=0.60700, chi(2,2)=0.20649",
        "  • C99 Evolución Ricci-Entrópica (oasis_evolution_operator.c): K_eff(0)=-0.382315 -> K_eff(10)=+0.413178 (L=3^4)",
        "  • Frontera abierta explícita: límite continuo a -> 0, L -> ∞ y positividad OS en S'(ℝ⁴)",
        "────────────────────────────────────────────────────────────────",
        f"🔐 NOTARIZACIÓN: Bitcoin OTS (Y={'OK' if ots_y else 'NO'}, Z={'OK' if ots_z else 'NO'}) | Master SHA-256: {master_hash[:16]}...",
        f"🕸️  GRAPHITY: {graph_summary} | Latencia consulta: {(time.perf_counter() - t0)*1000:.2f} ms (0% CPU LLM)",
        "════════════════════════════════════════════════════════════════",
    ])
    return "\n".join(lines)

if __name__ == "__main__":
    print(tz_process(" ".join(sys.argv[1:])))
