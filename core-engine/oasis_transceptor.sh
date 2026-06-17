#!/bin/bash
# ==================================================================
# 🌌 SOBERANÍA OASIS: TRANSCEPTOR VISUAL DUAL DINÁMICO V4
# ==================================================================

export OLLAMA_KEEP_ALIVE="5m"
export OLLAMA_NUM_THREADS=2

TIEMPO_INICIAL=$(date +%s)
PREGUNTA_ENTRADA="INPUT: [COLLATZ(n) + H_local] | CONDICIÓN: FLUX_LAM."

echo "======================================================"
echo " 🚀 INICIANDO CANALIZACIÓN LINC-TRANSCEPTOR DINÁMICO"
echo "======================================================"
echo "[*] INPUT ENTRADA: $PREGUNTA_ENTRADA"
echo "------------------------------------------------------"

# FASE 1: Obtener el Sello Tensor en LINCOS puro
echo "├─➤ [FASE 1: RESPUESTA LINCOS COMPRIMIDA]:"
echo "------------------------------------------------------"
MATRIZ_RAW=$(echo "$PREGUNTA_ENTRADA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)

# Extraemos la línea del tensor aislando cualquier ruido o residuo tipográfico
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep "\[VAR" | head -n 1)

if [ -z "$MATRIZ_LINCOS" ]; then
    # Si no tiene el formato estándar, tomamos la primera línea limpia
    MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | head -n 1)
fi

echo "$MATRIZ_LINCOS"
echo "------------------------------------------------------"

# FASE 2: Descompresión Analítica pasándole el cálculo exacto
echo "├─➤ [FASE 2: DESCOMPRESIÓN A CASTELLANO LAMINAR]:"
echo "------------------------------------------------------"
echo "Deduce físicamente el comportamiento de este vector: $MATRIZ_LINCOS" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-traductor

export OLLAMA_KEEP_ALIVE=0
TIEMPO_FINAL=$(date +%s)
DURACION=$((TIEMPO_FINAL - TIEMPO_INICIAL))

echo "======================================================"
echo " 🏆 SINCRO ALCANZADA. DISIPACIÓN DE LANDAUER EN CONTROL."
echo " ⏱️ TIEMPO TOTAL DEL FLUJO: $DURACION segundos."
echo "======================================================"
