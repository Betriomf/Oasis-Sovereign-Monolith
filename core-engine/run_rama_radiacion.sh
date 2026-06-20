#!/bin/bash
export OLLAMA_KEEP_ALIVE="5m"
PREGUNTA="INPUT: [Rad = Mp * exp(it)] | RESTRICCIÓN: Amortiguamiento crítico por T^2 en la frontera cuántica | TAREA: Calcula el escape geométrico de la radiación numérica para que la fricción tienda a cero. OUTPUT_START: [VAR ="

echo "======================================================"
echo " 🌌 RAMA LATERAL: CALCULA ESCAPE DE RADIACIÓN NUMÉRICA"
echo "======================================================"

MATRIZ_RAW=$(echo "$PREGUNTA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep -E "\[VAR|VAR =" | tail -n 1)

if [ -z "$MATRIZ_LINCOS" ]; then
    MATRIZ_LINCOS="[VAR = Rad * (T^2 / exp(it))]"
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
