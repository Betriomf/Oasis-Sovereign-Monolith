#!/usr/bin/env python3
"""Limpia codificación LaTeX, unifica kappa^2 = 5.3019, elimina duplicados y genera paquete Zenodo."""
import hashlib, re, sys
from pathlib import Path

def clean_tex(path_str: str):
    p = Path(path_str)
    if not p.exists():
        print(f"❌ No existe {p}. Pasa la ruta de tu archivo .tex como argumento.")
        return

    raw = p.read_bytes().decode("utf-8", errors="replace")

    # 1. Reparar mojibake UTF-8/GBK habitual y caracteres de control ASCII (\a -> \approx)
    fixes = {
        "Caball茅": "Caballé",
        "Navier鈥揝tokes": "Navier--Stokes",
        "\x07pprox": r"\approx",
        "–": "--",
        "—": "---",
    }
    for bad, good in fixes.items():
        raw = raw.replace(bad, good)
    raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", raw)

    # 2. Unificar kappa^2 = 5.3019 en todo el manuscrito
    raw = raw.replace("5.298", "5.3019")

    # 3. Eliminar texto duplicado después del primer \end{document}
    if r"\end{document}" in raw:
        raw = raw.split(r"\end{document}")[0] + "\\end{document}\n"

    out_tex = p.with_name(p.stem + "_zenodo_clean.tex")
    out_tex.write_text(raw, encoding="utf-8")

    sha = hashlib.sha256(out_tex.read_bytes()).hexdigest()
    sha_file = out_tex.with_suffix(".tex.sha256")
    sha_file.write_text(f"{sha}  {out_tex.name}\n", encoding="utf-8")

    print(f"✅ Manuscrito limpio guardado en : {out_tex}")
    print(f"🔒 Hash SHA-256 para Zenodo      : {sha}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "paper_a.tex"
    clean_tex(target)
