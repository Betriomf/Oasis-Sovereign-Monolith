#!/bin/bash
echo "======================================================"
echo " 🌐 ENJAMBRE OASIS: FILTRO BINARIO INTER-AGENTES"
echo "======================================================"

export OLLAMA_NUM_THREAD=2
export OLLAMA_KEEP_ALIVE=0

PREGUNTA_ORIGINAL="¿El colapso de Collatz al atractor (4,2,1) es un proceso adiabático de baja entropía?"

# FASE 1: Fijamos la matriz de preguntas nosotros para evitar el delirio de Qwen
P1="¿El borrado de bits en el ciclo de Collatz cumple con el Limite de Landauer? Contesta solo SI o NO:"
P2="¿Existe friccion termica en un procesador clasico x86_64 al procesar este flujo? Contesta solo SI o NO:"

echo "├─➤ [Fase 1]: Matrices de control fijadas en la memoria RAM."
echo -e "  P1: $P1\n  P2: $P2\n"

# FASE 2: Obligamos a Qwen a actuar como un interruptor binario puro (Masa minima)
echo "├─➤ [Fase 2]: Qwen dictamina el vector logico..."
R1=$(echo "$P1" | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b)
R2=$(echo "$P2" | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b)

echo "  Respuesta 1: $R1"
echo "  Respuesta 2: $R2"
echo "------------------------------------------------------"

# FASE 3: El peso pesado sintetiza el mapa de descarte
echo "└─➤ [Fase 3]: oasis-phi3-laminar genera la sintesis en Streaming..."
echo "Genera una conclusion breve sobre '$PREGUNTA_ORIGINAL' basandote estrictamente en que P1 dio como resultado ($R1) y P2 dio como resultado ($R2). Se directo." | /Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest

echo "======================================================"
echo " 🏆 BALÓN ASEGURADO. MANIFOLD EN PERFECTO EQUILIBRIO."
echo "======================================================"
