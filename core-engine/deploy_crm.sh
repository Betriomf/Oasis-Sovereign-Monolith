#!/bin/zsh
# 🌌 OASIS STACK: DESPLIEGUE DE TWENTY CRM (CAPA 22)

echo "⏳ Inicializando el motor del CRM en puerto local 8000..."

# Levantar Twenty CRM mapeando la base de datos local
docker run -d \
  --name oasis-crm \
  -p 8000:3000 \
  -e STORAGE_TYPE=local \
  -e DB_MODE=postgres \
  -e PG_DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/oasis_crm \
  --restart always \
  twentycrm/twenty:latest

echo "💎 CRM operativo en http://127.0.0.1:8000"
echo "📊 Base de datos vinculada al bus PostgreSQL. Flujo: LAMINAR."
