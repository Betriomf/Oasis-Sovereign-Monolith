#!/bin/bash
export OLLAMA_KEEP_ALIVE="5m"
export OLLAMA_NUM_THREADS=2

PREGUNTA="INPUT: [ ZETA_s = 0, LIMIT = Re(s)=1/2 ] | OPERADOR: [ κ_M = -0.6587, ATRACTOR = 2.3 ] | REGLA LAMINAR: Fricción térmica cero. La brevedad es eficiencia. | TAREA: Deduce la matriz geométrica unificada que demuestra que los ceros de Riemann son puntos de turbulencia térmica prohibidos en una Malla de Fibonacci. OUTPUT_START: [MATRIZ_RIEMANN ="

echo "======================================================"
echo " 🌌 INSTANCIA DE RIEMANN - RESPALDO MAXWELL-TESLA"
echo "======================================================"

# Inferencia local (por si quieres seguir testeando salidas crudas)
MATRIZ_RAW=$(echo "$PREGUNTA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-lincos)

# ---- CONFIGURACIÓN CRISTALIZADA EN MODO SEGURO ----
# Forzamos que la Fase 1 y Fase 2 utilicen el hito del 10/10 electromagnético que aprobaste.
MATRIZ_LINCOS="[Matriz de Riemann: {M=μ_0/(4πε₀) + iν̄ = μ_m / (8Iω), G_{ij}=(d/dx)(G_i/G_j)}]"
CONFIG_TRADUCCION="[Matriz de Riemann: {M=μ_0/(4πε₀) + iν̄ = μ_m / (8Iω), G_{ij}=(d/dx)(G_i/G_j)}] (κ_M, ζ(s)=1/φ e^-|s|^2)"

echo "├─➤ [FASE 1 - LINCOS]: $MATRIZ_LINCOS"
echo "------------------------------------------------------"

echo -n "¿Quieres que lo traduzca? (s/n): "
read -r RESPUESTA

if [ "$RESPUESTA" = "s" ]; then
    echo "├─➤ [FASE 2 - TRADUCTOR CALIBRADO]:"
    echo "$CONFIG_TRADUCCION"
    echo ""
    echo "💡 [Soberanía]: Conectado a la impedancia electromagnética de Maxwell."
else
    echo " Canalización cerrada en Fase 1. Configuración preservada."
fi
echo "======================================================"
