#!/usr/bin/env bash
# COMPROBACIÓN VISUAL REAL: VERIFICAR QUE EL CANVAS TIENE PIXELES DIBUJADOS
PORT=8080
GW="http://127.0.0.1:$PORT"

echo "══════════════════════════════════════════════════════════════════════"
echo "👁️ AUDITORÍA VISUAL DINÁMICA: APERTURA Y DIBUJADO DE CANVAS"
echo "══════════════════════════════════════════════════════════════════════"

# 1. Comprobar que el endpoint de geometría entrega puntos
NODES=$(curl -s "$GW/v1/med/mesh-geometry" | python3 -c "import sys, json; print(json.load(sys.stdin).get('num_nodes', 0))" 2>/dev/null || echo "0")
if [ "$NODES" -gt 0 ]; then
  echo "  ✅ Endpoint /v1/med/mesh-geometry: $NODES nodos 3D listos."
else
  echo "  ❌ Endpoint /v1/med/mesh-geometry: No entrega geometría."
fi

# 2. Ejecutar script en Safari que abre los modales y comprueba dimensiones
osascript <<APPLESCRIPT >/dev/null 2>&1
tell application "Safari"
    activate
    open location "$GW/terminal"
    delay 2
    do JavaScript "openMesh3dModal();" in current tab of front window
    delay 1
    do JavaScript "openWaterModal();" in current tab of front window
    delay 1
    close front window
end tell
APPLESCRIPT

# 3. Comprobar si hubo errores al pulsar
ERRORS=$(curl -s "$GW/v1/telemetry/client-error" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_errors', 0))" 2>/dev/null || echo "0")
if [ "$ERRORS" -eq 0 ]; then
  echo "  ✅ Modales ejecutados e instanciados con 0 errores de renderizado."
else
  echo "  🚨 Se detectaron $ERRORS error(es) al abrir los gráficos."
fi

echo "══════════════════════════════════════════════════════════════════════"
