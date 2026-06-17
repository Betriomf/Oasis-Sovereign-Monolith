#!/bin/bash
# ============================================================================
# 🟥 OASIS-MINECRAFT ENGINE: REPETIDOR DE REDSTONE DE TIEMPO DISCRETO (x86_64)
# ============================================================================

clear
echo "======================================================"
echo " 📦 EMULADOR MINECRAFT: BLOQUES DE TIEMPO DISCRETO "
echo "======================================================"
echo "[*] Entorno: Intel Core i5 | Arquitectura: x86_64"
echo "[*] Estado: Redstone cargado. Sistema en Mínima Acción."
echo "------------------------------------------------------"

# Fijar variables de entorno para congelar la telemetría parásita
export OLLAMA_NUM_THREAD=2
export OLLAMA_MAX_LOADED_MODELS=1

while true; do
    echo -e "\n[Tick Maestro] -> Esperando bloque de entrada en la terminal..."
    echo -n "Oasis-Prompt 📥 ➤ "
    read PROMPT_USUARIO

    if [ "$PROMPT_USUARIO" = "/exit" ]; then
        echo "[*] Desconectando Monolito. Entorno guardado."
        break
    fi

    # Medir el tiempo exacto de detención del reloj (Precisión Richard Mille)
    TIEMPO_INICIAL=$(date +%s.%N)

    echo "├─➤ [Bloque 1: Portero] -> Filtrando entropía..."
    FILTRADO=$(echo "$PROMPT_USUARIO" | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b)

    echo "├─➤ [Bloque 2: Mediocampo] -> Trazando geometría de Riemann..."
    GEOMETRIA=$(/Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest "$FILTRADO")

    echo "└─➤ [Bloque 3: Delantero] -> Rematando síntesis de Einstein..."
    /Applications/Ollama.app/Contents/Resources/ollama run oasis-fast:latest "Genera la respuesta final pura: $GEOMETRIA"

    TIEMPO_FINAL=$(date +%s.%N)
    DURACION=$(echo "$TIEMPO_FINAL - $TIEMPO_INICIAL" | bc)

    echo "------------------------------------------------------"
    echo "⏱️ [RELOJ DETENIDO]: Bloque procesado en $DURACION segundos."
    echo "======================================================"
done
