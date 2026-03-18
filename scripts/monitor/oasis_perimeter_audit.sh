#!/bin/bash
echo "🔍 AUDITORÍA PERIMETRAL: Escaneando conexiones activas..."
echo "----------------------------------------------------"
# Listamos conexiones ESTABLISHED filtrando procesos locales
CONEXIONES=$(netstat -atp tcp | grep -i "ESTABLISHED")

if [ -z "$CONEXIONES" ]; then
    echo "✅ PERÍMETRO LIMPIO: Sin fugas de datos externas."
else
    echo "⚠️  ALERTA: Conexiones detectadas:"
    echo "$CONEXIONES"
fi
echo "----------------------------------------------------"
