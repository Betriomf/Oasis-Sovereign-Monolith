#!/usr/bin/env python3
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lean_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".lean") and f != "lakefile.lean"]

print("=" * 68)
print("⚛️ [OASIS CORE]: AUDITORÍA MATEMÁTICA GLOBAL FORMAL (LEAN 4)")
print("=" * 68)

all_passed = True
for lf in sorted(lean_files):
    fpath = os.path.join(BASE_DIR, lf)
    res = subprocess.run(["lean", fpath], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  ✅ {lf.ljust(30)}: AXIOMÁTICAMENTE SELLADO (0 errores)")
    else:
        print(f"  ❌ {lf.ljust(30)}: FALLO FORMAL")
        print(res.stderr[:200])
        all_passed = False

print("-" * 68)
if all_passed:
    print("🏆 CERTIFICACIÓN FORMAL COMPLETA: Capa 0 validada al 100%.")
    sys.exit(0)
else:
    print("🛑 AUDITORÍA INCOMPLETA: Revise los módulos señalados.")
    sys.exit(1)
