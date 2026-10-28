#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS LEAN 4 AUDITOR & RED-TEAMING TEST
Valida compilación limpia sin 'sorry' y rechazo formal de teoremas falsos.
"""
import os, sys, subprocess, shutil, tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_lean_bin():
    lean_bin = shutil.which("lean")
    if not lean_bin:
        elan_lean = os.path.expanduser("~/.elan/bin/lean")
        if os.path.exists(elan_lean):
            return elan_lean
    return lean_bin

LEAN_BIN = find_lean_bin()

def run_positive_test(filepath):
    print(f"🔬 [LEAN 4 TEST]: Auditando '{os.path.basename(filepath)}'...")
    if not os.path.exists(filepath):
        print(f"❌ Error: {filepath} no existe.")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Rechazo si contiene la instrucción de evasión 'sorry'
    if "sorry" in content:
        print(f"❌ [REJECTED]: '{filepath}' contiene la instrucción 'sorry' (prueba incompleta).")
        return False

    res = subprocess.run([LEAN_BIN, filepath], capture_output=True, text=True, cwd=REPO_ROOT)
    if res.returncode != 0:
        print(f"❌ [FAIL]: Código de salida {res.returncode}:\n{res.stderr}")
        return False

    print(f"✅ [PASS]: '{os.path.basename(filepath)}' verificado por el kernel sin errores.")
    return True

def run_negative_test():
    print("🛡️ [RED TEAMING]: Comprobando rechazo formal de teoremas contradictorios...")
    # Teorema falso: pretende demostrar que 0 = 1 en Nat
    false_theorem = """
    theorem false_statement : (0 : Nat) = 1 := by
      rfl
    """
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as tmp:
        tmp.write(false_theorem)
        tmp_path = tmp.name

    try:
        res = subprocess.run([LEAN_BIN, tmp_path], capture_output=True, text=True)
        if res.returncode == 0:
            print("🚨 [CRITICAL ALERT]: El kernel aceptó un teorema falso. Auditoría fallida.")
            return False
        else:
            print("✅ [PASS]: El kernel de Lean 4 detectó el error lógico y rechazó la prueba.")
            return True
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    if not LEAN_BIN:
        print("❌ Error: Compilador Lean 4 no localizado en el PATH ni en ~/.elan/bin.")
        sys.exit(1)

    print(f"🛸 Usando Lean 4 binario: {LEAN_BIN}")
    t1 = run_positive_test(os.path.join(REPO_ROOT, "CapaZeroRiemann.lean"))
    t2 = run_positive_test(os.path.join(REPO_ROOT, "BiomedStability.lean"))
    t3 = run_negative_test()

    if t1 and t2 and t3:
        print("\n🏆 [RESULTADO]: Pipeline Lean 4 certificado (Valor comercial verificado).")
        sys.exit(0)
    else:
        print("\n❌ [RESULTADO]: Falló una o más pruebas del pipeline.")
        sys.exit(1)
