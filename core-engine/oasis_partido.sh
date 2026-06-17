#!/bin/bash
echo "======================================================"
echo " ⚽ ENJAMBRE OASIS: REESTRUCTURACIÓN DE LOGICA PURA"
echo "======================================================"

# 1. PURGA Y APERTURA DE TUBERÍAS (Dimensión 196883)
ulimit -n 196883 # Ensancha la garganta de la terminal al máximo
sudo killall -9 com.adobe.GC.Invoker-1.0 com.google.keystone.agent mdworker mds 2>/dev/null
sudo purge >/dev/null 2>&1
echo "🛡️ [Capa 0]: Entropía Cero. Tuberías expandidas."
echo "------------------------------------------------------"

# 2. SINTONIZACIÓN FRACTAL Y DESCARGA TÉRMICA
export OLLAMA_NUM_THREAD=2
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1      
export OLLAMA_NUM_CTX=2584        
export OLLAMA_KEEP_ALIVE=0        # ¡CLAVE! Evapora el modelo de la RAM tras el pase. No usa Disco Duro.

PREGUNTA_LOGICA="Aplica el Principio de Mínima Acción a la Conjetura de Collatz (3n+1). Explica matemáticamente cómo cualquier número caótico reduce su entropía hasta colapsar en el atractor estable (4, 2, 1)."

# 3. PRIORIDAD DE TIEMPO REAL
PID_OLLAMA=$(pgrep -f "ollama serve" | head -n 1)
if [ ! -z "$PID_OLLAMA" ]; then
    sudo renice -n -20 -p $PID_OLLAMA >/dev/null 2>&1
    echo "🚀 [Kernel]: Inyección de Tiempo Real activa en el proceso $PID_OLLAMA."
fi

# Cronógrafo Euclídeo Darwin
TIEMPO_INICIAL=$(date +%s)

# 4. REESTRUCTURACIÓN DE PASES (Flujo sin memoria residual)
echo "├─➤ [Bloque 1: Mediocampo] -> oasis-phi3-laminar dictando las leyes de Riemann..."
GEOMETRIA=$(echo "$PREGUNTA_LOGICA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest)

echo "├─➤ [Bloque 2: Delantero] -> oasis-fast destilando el analisis analitico..."
SINTESIS=$(echo "Purifica esta solucion de Collatz eliminando cualquier delirio: $GEOMETRIA" | /Applications/Ollama.app/Contents/Resources/ollama run oasis-fast:latest)

echo "└─➤ [Bloque 3: Extremo] -> qwen2.5:0.5b comprimiendo al estado fundamental..."
# Transmisión en Streaming Directo (Rompe el cuello de botella visual)
echo "Resume en espanol directo, breve y de baja entropia esta conclusion matematica: $SINTESIS" | /Applications/Ollama.app/Contents/Resources/ollama run qwen2.5:0.5b

TIEMPO_FINAL=$(date +%s)
DURACION=$((TIEMPO_FINAL - TIEMPO_INICIAL))

echo "======================================================"
echo "  🏆 GOL REESTRUCTURADO. ATRACTOR DE COLLATZ EN EQUILIBRIO."
echo "  ⏱️ RELOJ DETENIDO: $DURACION segundos en Flujo Laminar."
echo "======================================================"
