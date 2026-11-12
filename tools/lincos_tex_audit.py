#!/usr/bin/env python3
import sys, os, re

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("❌ Uso: lincos_tex_audit.py <archivo.tex>")
    sys.exit(1)

tex_path = sys.argv[1]
with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

errors = []

# Regla 1: Debe declarar explícitamente qué no se afirma (alcance honesto)
if "What is not claimed" not in content:
    errors.append("Falta subsección explícita 'What is not claimed'.")

# Regla 2: No puede afirmar solución incondicional al problema del Milenio
forbidden = [
    r"unconditional solution to the 3D",
    r"we prove global regularity",
    r"eliminates all singularities unconditionally"
]
for pat in forbidden:
    # Permitir solo si va precedido de 'do not claim' o 'do \emph{not} claim'
    for m in re.finditer(pat, content, re.IGNORECASE):
        context = content[max(0, m.start()-45):m.start()]
        if "not" not in context.lower():
            errors.append(f"Afirmación no acotada detectada: '{m.group(0)}'")

# Regla 3: Todo archivo .lean citado en \texttt{...lean} debe existir en el disco
lean_refs = re.findall(r'\\texttt\{([A-Za-z0-9_]+\.lean)\}', content)
for lf in set(lean_refs):
    if not os.path.exists(lf):
        errors.append(f"Archivo Lean citado en el paper pero ausente en el repo: {lf}")

if errors:
    print("❌ [LINCOS EPISTEMIC AUDIT]: FALLO")
    for e in errors:
        print(f"   • {e}")
    sys.exit(1)

print(f"✅ [LINCOS EPISTEMIC AUDIT]: APROBADO ({len(set(lean_refs))} módulos Lean verificados en disco, alcance honesto confirmado).")
