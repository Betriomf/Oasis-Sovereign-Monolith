#!/bin/sh
echo "🛡️ MONITOR DE CONEXIONES OASIS"
# Busca conexiones externas establecidas
externas=$(netstat -tun | grep -v "127.0.0.1" | grep "ESTABLISHED")
if [ -z "$externas" ]; then
    echo "✅ Silencio total. No hay fugas de datos hacia el exterior."
else
    echo "⚠️ ALERTA: Conexiones externas detectadas:"
    echo "$externas"
fi
