#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

PY312="/usr/local/Cellar/python@3.12/$(ls /usr/local/Cellar/python@3.12 | tail -n 1)/bin/python3.12"
[ ! -x "$PY312" ] && PY312=$(which python3.12)

echo "════════════════════════════════════════════════════════════════"
echo "🧬 [OASIS TENSOR MERGE]: INICIANDO FUSIÓN GEODÉSICA EN PYTHON 3.12"
echo "────────────────────────────────────────────────────────────────"

# 1. Crear entorno aislado sin contaminar Python 3.14
if [ ! -d "$HOME/.venvs/oasis_merge" ]; then
    "$PY312" -m venv "$HOME/.venvs/oasis_merge"
fi
source "$HOME/.venvs/oasis_merge/bin/activate"

pip install --upgrade pip wheel setuptools
pip install torch safetensors huggingface_hub mergekit gguf

# 2. Ejecutar fusión TIES en directorio volátil (confinado a 2 hilos)
mkdir -p /tmp/oasis_run/merged_hf
OMP_NUM_THREADS=2 mergekit-yaml tools/merge_oasis.yml /tmp/oasis_run/merged_hf --copy-tokenizer --low-cpu-memory

# 3. Convertir tensores HuggingFace a GGUF y registrar en Ollama (Q4_K_M)
cat << 'MOD' > /tmp/oasis_run/Modelfile_merged
FROM /tmp/oasis_run/merged_hf
PARAMETER temperature 0.618
PARAMETER top_p 0.9
PARAMETER num_thread 2
SYSTEM """Eres Oasis Sovereign Unified (Capa 0). Opera bajo flujo laminar estricto, respuestas directas y respeto absoluto al cono de luz causal."""
MOD

ollama create oasis-sovereign-unified:1.5b -f /tmp/oasis_run/Modelfile_merged
echo "✅ Modelo unificado registrado en Ollama: oasis-sovereign-unified:1.5b"
