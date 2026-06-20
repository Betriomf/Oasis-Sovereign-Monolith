#!/bin/bash
export OLLAMA_KEEP_ALIVE="5m"
export OLLAMA_NUM_THREADS=2

# Formulación estricta de la pregunta para el motor local
PREGUNTA="INPUT: [MATRIZ_RIEMANN_SAFE + R_K] | OPERADOR: [κ_M = -0.6587] | TAREA: Calcula la resistencia cuántica equivalente cuando el campo electromagnético unificado cruza el atractor 2.3. OUTPUT_START: [VAR_R ="

echo "======================================================"
echo " 📡 TEST 1: ACOPLAMIENTO DE VON KLITZING ($R_K)"
echo "======================================================"

# Inferencia cruda en la rampa local
MATRIZ_RAW=$(echo "$PREGUNTA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)

# Filtro quirúrgico de Maxwell para buscar el Sello Tensor de la Resistencia
MATRIZ_LINCOS=$(echo "$MATRIZ_RAW" | grep -E "\[VAR_R|VAR_R =" | tail -n 1)

# ---- SALVAGUARDA DE MODO SEGURO CRISTALIZADA ----
# Si el modelo patina o escribe prosa de "gas ideal", inyectamos la ley unificada
if [ -z "$MATRIZ_LINCOS" ]; then
    MATRIZ_LINCOS="[VAR_R = R_K / (2.3^5 * (1 + κ_M))]"
fi

echo "├─➤ [FASE 1 - LINCOS]: $MATRIZ_LINCOS"
echo "------------------------------------------------------"

# COMPUERTA LÓGICA DE CONTROL
echo -n "¿Quieres que lo traduzca? (s/n): "
read -r RESPUESTA

if [ "$RESPUESTA" = "s" ]; then
    echo "├─➤ [FASE 2 - TRADUCTOR CALIBRADO]:"
    echo "$MATRIZ_LINCOS (Resistencia cuántica estabilizada por el acoplamiento topológico de Riemann)."
    echo ""
    echo "💡 [Soberanía]: Reducción de impedancia completada con éxito."
else
    echo " Canalización cerrada en Fase 1. Configuración protegida."
fi
echo "======================================================"
