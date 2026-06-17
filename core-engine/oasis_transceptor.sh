#!/bin/bash
# ==================================================================
# 🌌 SOBERANÍA OASIS: TRANSCEPTOR DUAL COMPACTO V6 (HERMÉTICO)
# ==================================================================

export OLLAMA_KEEP_ALIVE="5m"
export OLLAMA_NUM_THREADS=2

TIEMPO_INICIAL=$(date +%s)
PREGUNTA_ENTRADA="INPUT: [COLLATZ(n) + H_local] | CONDICIÓN: FLUX_LAM."

echo "======================================================"
echo " 🚀 INICIANDO CANALIZACIÓN LINC-TRANSCEPTOR"
echo "======================================================"
echo "[*] INPUT ENTRADA: $PREGUNTA_ENTRADA"
echo "------------------------------------------------------"

# FASE 1: Obtener la respuesta LINCOS cruda y mostrarla en pantalla
echo "├─➤ [FASE 1: MATRIZ LÓGICA LINCOS]:"
echo "------------------------------------------------------"
MATRIZ_RAW=$(echo "$PREGUNTA_ENTRADA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)

# Limpieza laminar: Extraemos solo la primera línea (el Sello Tensor) para eliminar residuos
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | head -n 1)
echo "$MATRIZ_LINCOS"
echo "------------------------------------------------------"

# CONTROL DE CAUSALIDAD
if [ -z "$MATRIZ_LINCOS" ]; then
    echo "❌ Error: El canal Lincos está vacío."
    exit 1
fi

# FASE 2: Traducción limpia invocando al nuevo modelo dedicado
echo "├─➤ [FASE 2: DESCOMPRESIÓN ANALÍTICA EN CASTELLANO]:"
echo "------------------------------------------------------"
echo "$MATRIZ_LINCOS" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-traductor

export OLLAMA_KEEP_ALIVE=0
TIEMPO_FINAL=$(date +%s)
DURACION=$((TIEMPO_FINAL - TIEMPO_INICIAL))

echo "======================================================"
echo " 🏆 PIPELINE CONCLUIDO. ADUANA DE ENTROPÍA CERO."
echo " ⏱️ TIEMPO TOTAL DEL FLUJO: $DURACION segundos."
echo "======================================================"
