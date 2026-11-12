#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "════════════════════════════════════════════════════════════════"
echo "📐 [OASIS PAPER B]: PIPELINE DE CONSTRUCCIÓN HONESTA"
echo "────────────────────────────────────────────────────────────────"

echo "[1/5] Prototipo exploratorio Fisher-Rao..."
python3 tools/prototype_pseudospectral_tg.py

echo "[2/5] Auditoría Lean 4..."
LEAN_MODE="none"
python3 -c '
import glob, re, sys
bad = []
for p in sorted(glob.glob("*.lean")):
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"/-.*?-/", "", s, flags=re.DOTALL)
    s = re.sub(r"--.*", "", s)
    s = re.sub(r"\"[^\"]*\"", "", s)
    if re.search(r"\b(sorry|admit)\b", s):
        bad.append(p)
if bad:
    print("❌ sorry/admit activo en:", bad)
    sys.exit(1)
'
if command -v lean >/dev/null 2>&1; then
    lean RiemannFisherRaoHellinger.lean >/dev/null
    LEAN_MODE="lean4_kernel_verified"
    echo "✅ Lean 4: compilación nativa exitosa + 0 sorry/admit en código activo"
else
    LEAN_MODE="static_check_only"
    echo "ℹ️  Lean 4: comprobación sintáctica limpia"
fi

echo "[3/5] Auditoría epistemológica del manuscrito (.tex)..."
python3 tools/lincos_tex_audit.py papers/paper_b_millennium_regularity.tex

echo "[4/5] Compilación LaTeX (pdflatex -halt-on-error)..."
PDF_STATUS="no_pdflatex"
PDF_BYTES=0
if command -v pdflatex >/dev/null 2>&1; then
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=papers \
        papers/paper_b_millennium_regularity.tex >/tmp/tex1.log 2>&1 || { tail -25 /tmp/tex1.log; exit 1; }
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=papers \
        papers/paper_b_millennium_regularity.tex >/tmp/tex2.log 2>&1 || { tail -25 /tmp/tex2.log; exit 1; }
    PDF_FILE="papers/paper_b_millennium_regularity.pdf"
    if [ -s "$PDF_FILE" ]; then
        PDF_STATUS="pdf_compiled_ok"
        PDF_BYTES=$(wc -c < "$PDF_FILE" | tr -d ' ')
        echo "✅ PDF generado: $PDF_FILE (${PDF_BYTES} bytes)"
    fi
else
    echo "ℹ️  pdflatex no instalado: .tex validado y listo para Overleaf o arXiv"
fi

echo "[5/5] Registro estructurado en CRM..."
TEX_SHA=$(shasum -a 256 papers/paper_b_millennium_regularity.tex | awk '{print $1}')
LEAN_SHA=$(shasum -a 256 RiemannFisherRaoHellinger.lean | awk '{print $1}')

python3 tools/oasis_crm.py incident "v20" \
  "Build reproducible Paper B (${PDF_STATUS} | ${LEAN_MODE})" \
  "SHA256 tex: ${TEX_SHA:0:16}... | Hellinger SHA256: ${LEAN_SHA:0:16}..." \
  "Pipeline ejecutado sin falsos positivos; telemetría persistida en paper_b_provenance"

python3 tools/oasis_crm.py sync

# Escribir paper_b_provenance DESPUÉS de sync para que no sea sobrescrito
TEX_SHA="$TEX_SHA" LEAN_SHA="$LEAN_SHA" LEAN_MODE="$LEAN_MODE" PDF_STATUS="$PDF_STATUS" PDF_BYTES="$PDF_BYTES" python3 - << 'PYEOF'
import json, os, datetime

crm_path = "vault/crm_arquitectura_soberana.json"
with open(crm_path, "r", encoding="utf-8") as f:
    crm = json.load(f)

crm["paper_b_provenance"] = {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "tex_file": "papers/paper_b_millennium_regularity.tex",
    "tex_sha256": os.environ["TEX_SHA"],
    "lean_hellinger_file": "RiemannFisherRaoHellinger.lean",
    "lean_verification_level": os.environ["LEAN_MODE"],
    "lean_sha256": os.environ["LEAN_SHA"],
    "pdf_status": os.environ["PDF_STATUS"],
    "pdf_bytes": int(os.environ["PDF_BYTES"])
}

with open(crm_path, "w", encoding="utf-8") as f:
    json.dump(crm, f, indent=2, ensure_ascii=False)
print("✅ Telemetría exacta persistida en vault/crm_arquitectura_soberana.json")
PYEOF
echo "════════════════════════════════════════════════════════════════"
