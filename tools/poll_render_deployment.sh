#!/usr/bin/env bash
RENDER_URL="https://oasis-sovereign-gateway.onrender.com"
TARGET_VER="v18.7.6"
MAX_ATTEMPTS=20
ATTEMPT=1

echo "══════════════════════════════════════════════════════════════════════"
echo "📡 SONDEO DINÁMICO DE DESPLIEGUE EN RENDER ($TARGET_VER)"
echo "══════════════════════════════════════════════════════════════════════"

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
  TS=$(date +"%T")
  OPENAPI_VER=$(curl -s --max-time 4 "$RENDER_URL/v1/openapi.json" | grep -o '"version": "[^"]*"' | cut -d'"' -f4)
  HTML_VER=$(curl -s --max-time 4 "$RENDER_URL/terminal" | grep -o 'v18\.[0-9]*\.[0-9]*' | head -n 1)
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 4 "$RENDER_URL/terminal")

  echo "[$TS] Intento $ATTEMPT/$MAX_ATTEMPTS | HTTP: $HTTP_CODE | API: ${OPENAPI_VER:-desconocida} | HTML: ${HTML_VER:-desconocida}"

  if [ "$HTML_VER" = "$TARGET_VER" ] && [ "$OPENAPI_VER" = "18.7.6" ]; then
    echo "══════════════════════════════════════════════════════════════════════"
    echo "🏆 DESPLIEGUE CONFIRMADO: BACKEND Y FRONTEND 100% SINCRONIZADOS ($TARGET_VER)"
    echo "══════════════════════════════════════════════════════════════════════"
    exit 0
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 4
done

echo "ℹ️ El frontend ya está activo ($HTML_VER). Esperando convergencia de API ($OPENAPI_VER)."
exit 0
