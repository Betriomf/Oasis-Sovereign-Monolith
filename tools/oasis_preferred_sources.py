import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(".")
SOURCES_CFG = ROOT / "vault/preferred_sources.json"
DATASET = ROOT / "vault/datasets/oasis_crm_sft_dataset.jsonl"

DEFAULT_SOURCES = {
    "allowed_domains": [
        "github.com",
        "raw.githubusercontent.com",
        "zenodo.org",
        "doi.org",
        "arxiv.org",
        "leanprover-community.github.io",
    ],
    "pinned_references": [
        {
            "id": "paper_y_metrics",
            "instruction": "Cuáles son los valores numéricos exactos de K_int y K_proj del Paper Y en su(3), L=2^4 y L=3^4, y cuál es su límite de alcance?",
            "output": (
                "Valores del Paper Y: 1) su(3) puntual (N=2000): K_int=0.220498, K_proj=-0.440979 (min=-0.958835); "
                "2) Retículo L=2^4 (Cfg=200): K_int=0.198013, K_proj=-0.396026 (min=-0.875473); "
                "3) Retículo L=3^4 (Cfg=200): K_int=0.176612, K_proj=-0.353224 (min=-0.775408). "
                "Verificado en Lean 4.36.0 (PaperY_Entropy_Curvature_Margin.lean, 0 sorry) de forma condicional; "
                "NO demuestra existencia incondicional ni mass gap en el continuo R^4 o S'(R^4)."
            ),
            "source": "https://github.com/Betriomf/Oasis-Sovereign-Monolith/blob/main/papers/paper_y_orbit_curvature_entropy_bound.tex",
        },
        {
            "id": "lean4_mathlib_ref",
            "instruction": "Qué fuente oficial respalda la formalización en Lean 4 de Oasis Sovereign Monolith?",
            "output": "Los módulos en formal_proofs/ usan Lean 4.36.0 puro (0 sorry, 0 axiomas ocultos) y estructuras compatibles con Mathlib4.",
            "source": "https://leanprover-community.github.io/",
        },
    ],
}

def is_preferred_url(url: str, allowed_domains: list[str]) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in allowed_domains)

def sync_preferred_sources(new_url: str = "", title: str = "", summary: str = "") -> None:
    if SOURCES_CFG.exists():
        cfg = json.loads(SOURCES_CFG.read_text(encoding="utf-8"))
    else:
        cfg = DEFAULT_SOURCES
        SOURCES_CFG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if new_url:
        if not is_preferred_url(new_url, cfg["allowed_domains"]):
            raise ValueError(f"Dominio no permitido en fuentes preferidas: {new_url}")
        cfg["pinned_references"].append({
            "id": f"ref_{len(cfg['pinned_references']) + 1}",
            "instruction": f"Resume la fuente verificada: {title or new_url}",
            "output": summary.strip(),
            "source": new_url.strip(),
        })
        SOURCES_CFG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    existing = []
    if DATASET.exists():
        for ln in DATASET.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                row = json.loads(ln)
                if not str(row.get("source", "")).startswith("https://"):
                    existing.append(row)

    for ref in cfg["pinned_references"]:
        existing.append({
            "instruction": ref["instruction"],
            "input": "",
            "output": f"{ref['output']} [Fuente: {ref['source']}]",
            "source": ref["source"],
        })

    DATASET.parent.mkdir(parents=True, exist_ok=True)
    DATASET.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in existing) + "\n", encoding="utf-8")
    print(f"✅ Fuentes preferidas sincronizadas en {DATASET} ({len(existing)} entradas totales).")

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        sync_preferred_sources(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
    else:
        sync_preferred_sources()
