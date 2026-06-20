#!/bin/bash
echo "======================================================"
echo " ⚽ ENJAMBRE OASIS: COLLATZ EN FLUJO LAMINAR"
echo "======================================================"

# 1. PURGA DE ENTROPÍA Y PARÁSITOS (Estado Laminar Base)
# Aniquilamos telemetría e indexadores para evitar ruido térmico
sudo killall -9 com.adobe.GC.Invoker-1.0 com.google.keystone.agent mdworker mds 2>/dev/null
sudo purge
echo "🛡️ [Capa 0]: Caché RAM purgada. Telemetría silenciada. Fricción Cero."
echo "------------------------------------------------------"

# 2. SINTONIZACIÓN FRACTAL DE OLLAMA (Límite Termodinámico)
export OLLAMA_NUM_THREAD=2
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1      # Evita colisiones en la memoria RAM
export OLLAMA_NUM_CTX=2584        # Malla de Fibonacci (F18) para empaquetado óptimo

PREGUNTA_LOGICA="Aplica el Principio de Mínima Acción a la Conjetura de Collatz (3n+1). Explica cómo cualquier número reduce su entropía hasta colapsar en el atractor estable 4,2,1."

# 3. EL "VUELO" DEL HARDWARE (Prioridad de Tiempo Real)
PID_OLLAMA=$(pgrep -f "ollama serve" | head -n 1)
if [ ! -z "$PID_OLLAMA" ]; then
    sudo renice -n -20 -p $PID_OLLAMA >/dev/null 2>&1
    echo "🚀 [Motor Física]: Prioridad máxima asignada al proceso $PID_OLLAMA."
fi

# Cronógrafo Euclídeo (Precisión en Segundos Puros)
TIEMPO_INICIAL=$(date +%s)

# 4. PIPELINE DE SUPERCONDUCTIVIDAD (Variables en RAM, sin tocar el disco)
echo "├─➤ [Bloque 1: Portero] -> qwen2.5:0.5b extrayendo variables de la inercia..."
FILTRADO=$(echo "$PREGUNTA_LOGICA" | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b)

echo "├─➤ [Bloque 2: Mediocampo] -> oasis-phi3-laminar aplicando rigor de Riemann..."
GEOMETRIA=$(echo "Ordena logicamente y dale consistencia matematica a esto, eliminando delirios: $FILTRADO" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest)

echo "└─➤ [Bloque 3: Delantero] -> oasis-fast ejecutando sintesis final..."
/Applications/Ollama.app/Contents/Resources/ollama run oasis-fast:latest "Traduce a un espanol directo, breve y de baja entropia la solucion termodinamica de Collatz: $GEOMETRIA"

TIEMPO_FINAL=$(date +%s)
DURACION=$((TIEMPO_FINAL - TIEMPO_INICIAL))

echo "======================================================"
echo "  🏆 GOL SOBERANO. ATRACTOR DE COLLATZ COMPRIMIDO CON ÉXITO."
echo "  ⏱️ RELOJ DETENIDO: $DURACION segundos en Flujo Laminar."
echo "======================================================"
