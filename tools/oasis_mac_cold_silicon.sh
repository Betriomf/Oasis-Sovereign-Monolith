#!/usr/bin/env bash
set -euo pipefail

echo "❄️  [OASIS SILICIO FRÍO — PERFIL MACBOOK AIR (PAPERS C/D/E)]"

# 1. Aumentar límite de descriptores en sesión actual (inspirado en Pilar 86 / Ring-3)
ulimit -n 65536 2>/dev/null || true

# 2. Exportar variables de contención térmica y KV-Cache mínimo para Ollama local
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_KEEP_ALIVE="3m"
export OMP_NUM_THREADS=2

# 3. Reiniciar demonio Ollama con el perfil de bajo consumo si está corriendo
if pgrep -x "ollama" >/dev/null 2>&1; then
  pkill -x "ollama" || true
  sleep 1
fi
nohup ollama serve >/tmp/ollama_cold_silicon.log 2>&1 &
sleep 2

echo "✅ Ollama activo en modo Silicio Frío (2 hilos, 1 modelo en RAM, descarga automática tras 3 min)."
echo "✅ Límite de descriptores en sesión: $(ulimit -n)"
echo "✅ Memoria libre/activa verificada:"
vm_stat | head -n 6
