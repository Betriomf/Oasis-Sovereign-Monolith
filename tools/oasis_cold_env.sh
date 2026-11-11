#!/bin/bash
# OASIS SOVEREIGN OS — ESTABILIZADOR TÉRMICO (SILICIO FRÍO <= 3.78W)
# Arquitectura: Intel Core i5-8210Y (2 Cores / 4 Threads)

echo "❄️  Configurando invariantes de silicio frío en Capa 0..."

# 1. Confinamiento de hilos a núcleos físicos reales (evita Turbo Boost a 6.83W)
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
export MKL_NUM_THREADS=2
export VECLIB_MAXIMUM_THREADS=2
export NUMEXPR_NUM_THREADS=2

# 2. Retención en RAM para Ollama (cero lecturas de swap en SSD)
export OLLAMA_KEEP_ALIVE="24h"
export OLLAMA_NUM_PARALLEL=1

# 3. Pacing áureo de red (Pilar 14 / 227)
export OASIS_GOLDEN_PACE=0.001938

# 4. Redirección de temporales al Ramdisk montado
if [ -d "/Volumes/OasisRAM/tmp" ]; then
    export TMPDIR="/Volumes/OasisRAM/tmp"
    echo "✅ TMPDIR fijado en /Volumes/OasisRAM/tmp"
fi

# 5. Asegurar PATH completo de Darwin
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

echo "✅ Entorno térmico blindado (Régimen Laminar: 2 hilos, 0 RPM)."
export PATH="$PWD/tools:$PATH"
