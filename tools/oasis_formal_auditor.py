#!/usr/bin/env python3
"""
Auditor Formal Optimizado para Oasis Sovereign Monolith (Lean 4).
Verifica compilación pura (Capa 0) y ausencia estricta de 'sorry' (Capa 1) en < 2 segundos.
"""
import re
import subprocess
import sys
from pathlib import Path

def find_lean_files():
    excluded = {"lakefile.lean", "lakefile.toml"}
    files = [p for p in Path(".").glob("*.lean") if p.name not in excluded]
    files += list(Path("formal_proofs").glob("*.lean"))
    return sorted(set(files))

def audit_file(path: Path) -> tuple[bool, str]:
    raw = path.read_text(encoding="utf-8")
    no_block = re.sub(r"/-.*?-/", "", raw, flags=re.S)
    no_comments = re.sub(r"--.*", "", no_block)
    no_comments = re.sub(r'"[^"]*"', '""', no_comments)

    if re.search(r"\bsorry\b", no_comments):
        return False, "Capa 1 FALLIDA: Contiene 'sorry' sin demostrar."

    res = subprocess.run(["lean", str(path)], capture_output=True, text=True, timeout=45)
    if res.returncode != 0:
        err = (res.stderr or res.stdout).strip()
        return False, f"Capa 0 FALLIDA:\n{err}"

    return True, "AXIOMÁTICAMENTE SELLADO (0 errores, 0 sorry)"

def main():
    files = find_lean_files()
    print("════════════════════════════════════════════════════════════════════")
    print(f"⚛️  [OASIS FORMAL AUDITOR]: Verificando {len(files)} módulos Lean 4")
    print("════════════════════════════════════════════════════════════════════")
    all_ok = True
    for f in files:
        ok, msg = audit_file(f)
        if ok:
            print(f"  ✅ {str(f):<42} | {msg}")
        else:
            all_ok = False
            print(f"  ❌ {str(f):<42} | {msg}")

    print("────────────────────────────────────────────────────────────────────")
    if not all_ok:
        print("🛑 AUDITORÍA BLOQUEADA: Hay errores formales.")
        sys.exit(1)
    print(f"🏆 CERTIFICACIÓN COMPLETA: {len(files)}/{len(files)} módulos validados al 100%.")

if __name__ == "__main__":
    main()
