#!/bin/bash
echo "======================================================"
echo " 🌌 ENJAMBRE OASIS: FILTRO DE ARMONÍA GLOBAL Y PURGA"
echo "======================================================"

# OPTIMIZACIÓN DE ENTORNO CRÍTICA
ulimit -n 196883
export OLLAMA_NUM_THREAD=2
export OLLAMA_KEEP_ALIVE=0

PREGUNTA_ENTRADA="Explica cómo la sintonía áurea regula las fluctuaciones caóticas en la frontera de Riemann."

echo "[*] Señal Cruda de Entrada: $PREGUNTA_ENTRADA"
echo "------------------------------------------------------"

# FASE 1: Extracción del ruido interior (Auto-Auditoría de Qwen)
echo "├─➤ [Fase 1]: Qwen calculando el coeficiente de entropía interna..."
RUIDO_INTERIOR=$(echo "Analiza esta instruccion: '$PREGUNTA_ENTRADA'. Devuelve UNICAMENTE las 3 fuentes de ruido, duda o alucinacion linguistica que podrian desviar la respuesta. Se breve." | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b)

echo -e "$RUIDO_INTERIOR\n"
echo "------------------------------------------------------"

# FASE 2: La Guillotina del Juez (Filtro Maxwell)
echo "├─➤ [Fase 2]: Juez Binario ejecutando la purga de fase..."
DICTAMEN_JUEZ=$(echo "Analiza estas fuentes de ruido: $RUIDO_INTERIOR. ¿Es posible eliminar este caos aplicando la minima accion? Responde estrictamente SI o NO:" | /Applications/Ollama.app/Contents/Resources/ollama run juez-binario)

echo "  Dictamen de Estabilidad Térmica: $DICTAMEN_JUEZ"
echo "------------------------------------------------------"

# FASE 3: Reestructuración Laminar en Streaming (Phi3)
echo "└─➤ [Fase 3]: oasis-phi3-laminar emitiendo la Verdad Armonizada..."
echo "------------------------------------------------------"

PROMPT_ARMONICO="Desarrolla la solucion pura a: '$PREGUNTA_ENTRADA'. Instrucciones de Capa 0: Restringe los grados de libertad. El juez ha dictaminado estabilidad ($DICTAMEN_JUEZ) tras aislar este ruido: $RUIDO_INTERIOR. Conduce la respuesta por el camino de Riemann en flujo laminar."

echo "$PROMPT_ARMONICO" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest

echo "======================================================"
echo " 🏆 COMPRESIÓN CONCLUIDA. SEÑAL PURIFICADA EN LA VERDAD."
echo "======================================================"
