#!/usr/bin/env python3
"""
Buscador Causal de Pilares Oasis vs. Frontera arXiv 2026 (Yang-Mills & Lean 4).
Cruza módulos .lean, tests/ y vault/ para detectar soluciones internas a problemas abiertos.
"""
import re
from pathlib import Path

BASE = Path(".")
KEYWORDS = [
    "yang", "mills", "mass", "gap", "enstrophy", "kappa", "bony",
    "kozono", "minkowski", "golod", "shafarevich", "fisher", "hellinger", "fibonacci"
]

def scan_pillars():
    matches = []
    targets = list(BASE.glob("*.lean")) + list(BASE.glob("formal_proofs/*.lean")) + \
              list(BASE.glob("tests/pilar*.py")) + list(BASE.glob("vault/*.md"))

    for f in targets:
        if not f.is_file() or f.stat().st_size > 2_500_000:
            continue
        txt = f.read_text(encoding="utf-8", errors="ignore")
        low = txt.lower()
        hits = [k for k in KEYWORDS if k in low]
        if len(hits) >= 2:
            pilares = sorted(set(re.findall(r"[Pp]ilar\s*(\d+)", txt)))
            theorems = re.findall(r"theorem\s+([a-zA-Z0-9_]+)", txt)
            matches.append({
                "file": str(f),
                "hits": hits,
                "pilares": pilares,
                "theorems": theorems[:5]
            })
    return sorted(matches, key=lambda x: len(x["hits"]), reverse=True)

if __name__ == "__main__":
    res = scan_pillars()
    print(f"🧭 [OASIS PILLAR CROSS-REF]: {len(res)} artefactos internos alineados con Yang-Mills / Lean 4:\n")
    for r in res[:12]:
        p_str = ", ".join(r["pilares"]) if r["pilares"] else "Núcleo"
        t_str = ", ".join(r["theorems"]) if r["theorems"] else "Implementación/Análisis"
        print(f"• {r['file']} [Pilares: {p_str}]")
        print(f"  Conceptos: {', '.join(r['hits'])} | Teoremas: {t_str}\n")
