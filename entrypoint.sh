#!/bin/bash
set -e

# Ajustar puerto de Nginx al asignado por Render (o 8080 por defecto)
PORT=${PORT:-8080}
sed -i "s/listen 8080;/listen $PORT;/g" /etc/nginx/nginx.conf

echo "🛰️ [OASIS DOCKER BOOT]: Arrancando ttyd en 127.0.0.1:7681..."
ttyd -p 7681 -b /ttyd -W /bin/bash &

echo "🛰️ [OASIS DOCKER BOOT]: Arrancando Oasis Gateway en 127.0.0.1:8000..."
PORT=8000 python3 agents_core/oasis_render_gateway.py &

echo "🛰️ [OASIS DOCKER BOOT]: Iniciando proxy inverso Nginx en puerto $PORT..."
exec nginx -g "daemon off;"
