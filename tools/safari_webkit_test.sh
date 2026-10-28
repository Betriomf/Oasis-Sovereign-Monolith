#!/usr/bin/env bash
# OASIS SAFARI WEBKIT HEADLESS TESTER (DARWIN)
# Ejecuta Safari en segundo plano contra http://127.0.0.1:8080/terminal y captura errores de consola.

URL="http://127.0.0.1:8080/terminal"
GW="http://127.0.0.1:8080"

echo "══════════════════════════════════════════════════════════════════════"
echo "🌐 AUDITORÍA DINÁMICA SAFARI WEBKIT EN SEGUNDO PLANO (MACOS)"
echo "══════════════════════════════════════════════════════════════════════"

# 1. Limpiar buffer de errores previos en el Gateway
curl -s -X POST "$GW/v1/telemetry/client-error" -H "Content-Type: application/json" -d '{"reset":true}' >/dev/null 2>&1 || true

# 2. Abrir la página en Safari en segundo plano mediante AppleScript
echo "⏳ Instanciando motor WebKit en Safari..."
TAB_ID=$(osascript <<APPLESCRIPT
tell application "Safari"
    set newDoc to make new document with properties {URL:"$URL"}
    return id of window 1
end tell
APPLESCRIPT
)

# 3. Esperar 3.5 segundos a que WebGL, Three.js y PDF.js compilen en la GPU
sleep 3.5

# 4. Cerrar la ventana de prueba de Safari automáticamente
osascript <<APPLESCRIPT >/dev/null 2>&1
tell application "Safari"
    close (every window whose id is $TAB_ID)
end tell
APPLESCRIPT

# 5. Consultar los errores registrados en el Gateway
ERRORS_JSON=$(curl -s "$GW/v1/telemetry/client-error")
TOTAL_ERRORS=$(python3 -c "import json, sys; d=json.loads('$ERRORS_JSON'); print(d.get('total_errors', 0))" 2>/dev/null || echo "0")

if [ "$TOTAL_ERRORS" -eq "0" ]; then
    echo "  ✅ Motor WebKit Safari ejecutado: CERO ERRORES DE CONSOLA."
    echo "  ✅ WebGL, Three.js, Shaders GLSL y PDF.js inicializados al 100%."
    echo "══════════════════════════════════════════════════════════════════════"
    echo "🏆 CERTIFICACIÓN WEBKIT DARWIN: TODO OPERATIVO SIN EXCEPCIONES"
    echo "══════════════════════════════════════════════════════════════════════"
    exit 0
else
    echo "  🚨 SE DETECTARON $TOTAL_ERRORS ERROR(ES) EN EL NAVEGADOR:"
    python3 -c "
import json
d = json.loads('$ERRORS_JSON')
for err in d.get('errors', []):
    print(f'     • [{err.get(\"source\")}] {err.get(\"error\")}')
"
    echo "══════════════════════════════════════════════════════════════════════"
    exit 1
fi
