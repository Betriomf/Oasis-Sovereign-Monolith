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
if command -v lake >/dev/null 2>&1 && [ -f lakefile.lean ]; then
    if lake build >/tmp/lake_build.log 2>&1; then
        if grep -rnE "\b(sorry|admit)\b" --include="*.lean" . >/dev/null 2>&1; then
            echo "❌ lake build compiló pero contiene sorry/admit"
            exit 1
        fi
        LEAN_MODE="lake_build_verified"
        echo "✅ Lean 4: lake build exitoso + 0 sorry/admit"
    else
        echo "❌ lake build falló (ver /tmp/lake_build.log)"
        exit 1
    fi
else
    if grep -rnE "\b(sorry|admit)\b" --include="*.lean" . >/dev/null 2>&1; then
        echo "❌ grep: detectado sorry/admit en *.lean"
        exit 1
    fi
    LEAN_MODE="static_grep_only_no_lake"
    echo "ℹ️  Lean 4: lake/Mathlib ausente en entorno local -> solo grep estático limpio (NO compilación formal)"
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
    else
        echo "❌ pdflatex terminó sin generar PDF válido"
        exit 1
    fi
else
    echo "ℹ️  pdflatex no instalado: .tex validado y listo para compilación externa"
fi

echo "[5/5] Registro estructurado en CRM..."
TEX_SHA=$(shasum -a 256 papers/paper_b_millennium_regularity.tex | awk '{print $1}')
LEAN_SHA=$(shasum -a 256 RiemannFisherRaoHellinger.lean | awk '{print $1}')

python3 - << PYEOF
import json, os, datetime

crm_path = "vault/crm_arquitectura_soberana.json"
if os.path.exists(crm_path):
    with open(crm_path, "r", encoding="utf-8") as f:
        crm = json.load(f)
else:
    crm = {}

crm["paper_b_provenance"] = {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "tex_file": "papers/paper_b_millennium_regularity.tex",
    "tex_sha256": "${TEX_SHA}",
    "lean_hellinger_file": "RiemannFisherRaoHellinger.lean",
    "lean_verification_level": "${LEAN_MODE}",
    "lean_sha256": "${LEAN_SHA}",
    "pdf_status": "${PDF_STATUS}",
    "pdf_bytes": int("${PDF_BYTES}")
}

with open(crm_path, "w", encoding="utf-8") as f:
    json.dump(crm, f, indent=2, ensure_ascii=False)
print("✅ Telemetría exacta asentada en vault/crm_arquitectura_soberana.json")
PYEOF

python3 tools/oasis_crm.py incident "v20" \
  "Build reproducible Paper B (${PDF_STATUS} | ${LEAN_MODE})" \
  "SHA256 tex: ${TEX_SHA:0:16}... | Hellinger ℝ SHA256: ${LEAN_SHA:0:16}..." \
  "Pipeline ejecutado sin falsos positivos; estado real registrado en paper_b_provenance"

python3 tools/oasis_crm.py sync
echo "════════════════════════════════════════════════════════════════"
