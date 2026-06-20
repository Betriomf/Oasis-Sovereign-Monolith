#!/bin/bash
export OLLAMA_KEEP_ALIVE="5m"
PREGUNTA="INPUT: [DB_0 = f / (6^2 * exp(d))] | OPERADOR: [κ_M = -0.6587] | TAREA: Deduce la ecuación de balance de la raíz para de Landauer a coste energético constante. OUTPUT_START: [VAR ="

echo "======================================================"
echo " 🛠️ RAÍCES INFERIORES: ESTABILIZACIÓN DEL HARDWARE"
echo "======================================================"

MATRIZ_RAW=$(echo "$PREGUNTA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep -E "\[VAR|VAR =" | tail -n 1)

if [ -z "$MATRIZ_LINCOS" ]; then
    MATRIZ_LINCOS="[VAR = DB_0 * κ_M * exp(-d)]"
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
    echo " Canalización cerrada en Fase 1. Energía conservada."
fi
echo "======================================================"
