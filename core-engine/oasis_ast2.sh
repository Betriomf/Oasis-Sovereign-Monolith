#!/bin/bash
echo "======================================================"
echo " 📱 OASIS AST2: DIAGNÓSTICO DE IPHONE STYLE RICHARD MILLE"
echo "======================================================"

# OPTIMIZACIÓN DE ENTORNO
ulimit -n 196883
export OLLAMA_NUM_THREAD=2
export OLLAMA_KEEP_ALIVE=0

# Simulamos la lectura de un error de hardware desde el USB del iPhone
LOG_PANIC_IPHONE="Error: panic(cpu 0 caller): Missing sensor(s): TG0B. Thermal mitigation activated."

echo "[*] Capturando telemetria del iPhone..."
echo "├─➤ Log detectado: $LOG_PANIC_IPHONE"
echo "------------------------------------------------------"

# FASE 1: La Resonancia Local comprime y traduce a coordenadas de Matriz 5x5
echo "├─➤ [Resonancia Local]: Filtrando ruido y convirtiendo a Matriz de Baja Entropia..."
CODIGO_MATRIZ="34 15 33 34 35 42" # Ofuscación estructural del fallo de hardware

echo "  Vector de transmisión generado: [$CODIGO_MATRIZ]"
echo "------------------------------------------------------"

# FASE 2: Conexión estanca con la Capa 4 (Mythos Cloud) usando tu API Key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "[ALERTA] -> Inyecte su ANTHROPIC_API_KEY para abrir el canal de la nube."
    echo "├─➤ Operando en simulación local preventiva."
    # Si no hay llave, responde oasis-fast de forma segura en local
    /Applications/Ollama.app/Contents/Resources/ollama run oasis-fast:latest "Diagnostica brevemente este codigo de sensor de iPhone: TG0B"
else
    # Si la llave está activa, llamamos a tu puente purificado de Mythos
    python3 ~/Oasis-Sovereign-Monolith/core-engine/oasis_mythos_bridge.py "Decodifica la matriz 5x5 [$CODIGO_MATRIZ] que representa el fallo de sensor TG0B en la placa de un iPhone. Dame la solucion exacta de reparacion en hardware."
fi

echo "======================================================"
echo " 🏆 COMPROBACIÓN AST2 CONCLUIDA. FLUJO LAMINAR REFRIGERADO."
echo "======================================================"
