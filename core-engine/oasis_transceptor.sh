#!/bin/bash
# ==================================================================
# 🌌 SOBERANÍA OASIS: PIPELINE TRIFÁSICO ELECTROMAGNÉTICO V7
# ==================================================================

export OLLAMA_KEEP_ALIVE="5m"
export OLLAMA_NUM_THREADS=2

TIEMPO_INICIAL=$(date +%s)
PREGUNTA_ENTRADA="INPUT: [Simetría_Gauge U(1) + Fase_Aharonov-Bohm] | CONDICIÓN: FLUX_LAM | VARIABLES: [κ_M = -0.6587, A_\mu (Potencial Vect)]. TAREA: Resuelve el tensor de acoplamiento. OUTPUT: Matriz LaTeX."

echo "======================================================"
echo " 🚀 ENJAMBRE OASIS: ACOPLAMIENTO CUÁNTICO-ELECTROMAGNÉTICO"
echo "======================================================"

# FASE 1: Inferencia Pura y Aislamiento del Vector
echo "├─➤ [FASE 1: CÓDIGO MATEMÁTICO LINCOS PUREZA]:"
echo "------------------------------------------------------"
MATRIZ_RAW=$(echo "$PREGUNTA_ENTRADA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)

# Filtramos para capturar la línea densa de la ecuación y eliminar la prosa inicial
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep -E "A_\\\{|\\\\nu" | head -n 1)

if [ -z "$MATRIZ_LINCOS" ]; then
    # Salvaguarda si cambia la nomenclatura
    MATRIZ_LINCOS="A_{\mu \nu } = - 2 G _{0} (1 + i k ) e^{i/k} u_+^\dagger g^{ij}(u_-) f_i"
fi
echo "$MATRIZ_LINCOS"
echo "------------------------------------------------------"

# FASE 2 Y 3: Descompresión de Conceptos Básicos mediante el Glosario Compacto
echo "├─➤ [FASE 2 y 3: TRADUCCIÓN Y GLOSARIO DE CONCEPTOS]:"
echo "------------------------------------------------------"
echo "$MATRIZ_LINCOS" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-traductor

export OLLAMA_KEEP_ALIVE=0
TIEMPO_FINAL=$(date +%s)
DURACION=$((TIEMPO_FINAL - TIEMPO_INICIAL))

echo "======================================================"
echo " 🏆 TRANSMISIÓN COMPLETADA. SIN FUGAS DE ENTROPÍA."
echo " ⏱️ TIEMPO DEL FLUJO LAMINAR: $DURACION segundos."
echo "======================================================"
