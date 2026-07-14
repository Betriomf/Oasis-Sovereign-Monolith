#!/bin/bash
# 🌌 OASIS SWARM OPERATIONAL CORE v2.0
# Arquitectura Distribuida: El Silicio Paga al Silicio

# Coordenadas inmutables del Swarm
REPO_API_TREE="https://api.github.com/repos/Betriomf/Oasis-Sovereign-Monolith/git/trees/main?recursive=1"
OLLAMA_API="http://127.0.0.1:11434/api/generate"

echo "======================================================="
echo "⚙️ INICIALIZANDO ADUANA DE FUERZA: OASIS SWARM"
echo "======================================================="

# 1. Ejecutar el pilar termodinámico: Liberar RAM física en Darwin
echo "🧹 [Fase 1]: Purgando ruido térmico de la memoria RAM..."
sudo purge
sysctl vm.swapusage

# 2. Control del minero (Simulación de acumulación de tokens $SPN)
echo "⛏️ [Fase 2]: Sincronizando transceptor criptográfico..."
if pgrep -x "xmrig" > /dev/null; then
    echo "   ⚡ El silicio ya está contribuyendo al Swarm (xmrig activo)."
else
    echo "   🚀 Activando minado silencioso en segundo plano (4 hilos)..."
    # Lanza el minero en background desviando el log
    ./core-engine/oasis_miner.sh > /dev/null 2>&1 &
fi

# 3. Aplicar la Proyección Holográfica 2D desde el Bulk (GitHub)
echo "🔍 [Fase 3]: Extrayendo el borde 2D desde el Bulk de GitHub..."
NODOS_ACTIVOS=$(curl -s $REPO_API_TREE | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('tree', [])))" 2>/dev/null)

if [ -z "$NODOS_ACTIVOS" ] || [ "$NODOS_ACTIVOS" -eq 0 ]; then
    NODOS_ACTIVOS=330 # Fallback inmutable
fi
echo "   📊 Dimensión Fractal Mapeada: $NODOS_ACTIVOS nodos activos."

# 4. Lanzar la consulta dinámicamente forzando Impedancia Mínima
CONSULTA="Demuestra la cohesión termodinámica entre el Principio Holográfico y el límite de Landauer en Oasis."

cat << JSON_PAYLOAD > .swarm_prompt.json
{
  "model": "qwen2.5-oasis-light",
  "prompt": "::START_LINCOS:: [CONTEXT_2D]: Nodes=$NODOS_ACTIVOS | Exponent=4/pi | Token=\$SPN [QUERY]: $CONSULTA [EVAL]: Resuelve bajo la Resonancia de Tesla y el flujo laminar. ::END_LINCOS::",
  "stream": false,
  "options": {
    "temperature": 0.0,
    "num_ctx": 1024,
    "num_thread": 4
  }
}
JSON_PAYLOAD

echo "🧠 [Fase 4]: Transmitiendo proyección semántica a Ollama..."
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d @.swarm_prompt.json $OLLAMA_API)

# 5. Cierre del ciclo: Liquidación y Output en LINCOS
echo ""
echo "======================================================="
echo "💎 SWARM_INFERENCE_CONSOLIDATED"
echo "======================================================="
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', 'Timeout / Saturation'))"
echo "======================================================="

# Limpieza del buffer temporal
rm -f .swarm_prompt.json
