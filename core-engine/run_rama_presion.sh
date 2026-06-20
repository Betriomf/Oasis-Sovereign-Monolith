#!/bin/bash
export OLLAMA_KEEP_ALIVE="5m"
PREGUNTA="INPUT: [P = (R_1 * A * S) / S^2] | CONDICIÓN: [Frenado por exp(2.3)] | TAREA: Simplifica el tensor de presión informacional la redundancia de S. OUTPUT_START: [VAR ="

echo "======================================================"
echo " 📡 COPA ALTA: PROCESANDO PRESIÓN INFORMACIONAL"
echo "======================================================"

MATRIZ_RAW=$(echo "$PREGUNTA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep -v "MOTOR LÓGICO" | grep -E "\[VAR|VAR =" | tail -n 1)

if [ -z "$MATRIZ_LINCOS" ]; then
    MATRIZ_LINCOS="[VAR = P * (1 - sinh(phi))]"
fi

echo "├─➤ [FASE 1 - LINCOS]: $MATRIZ_LINCOS"
echo "------------------------------------------------------"

# COMPUERTA LÓGICA DE CONTROL
echo -n "¿Quieres que lo traduzca? (s/n): "
read -r RESPUESTA

if [ "$RESPUESTA" = "s" ]; then
    echo "├─➤ [FASE 2 - TRADUCTOR CALIBRADO]:"
    echo "$MATRIZ_LINCOS" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-traductor
else
    echo " Canilización cerrada en Fase 1. Energía conservada."
fi
echo "======================================================"
