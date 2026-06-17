#!/bin/bash
echo "❄️ INICIANDO PROTOCOLO HAFNIO DE ARRANQUE..."

# Esperamos a que el sistema cargue todos los procesos tras el reinicio
sleep 30

# Congelamos la telemetría y el ruido térmico por nombre, SIN usar sudo
killall -STOP "Siri" 2>/dev/null
killall -STOP "CleanMyMac X" 2>/dev/null
killall -STOP "CleanMyMac X Menu" 2>/dev/null
killall -STOP "cloudd" 2>/dev/null
killall -STOP "nsurlsessiond" 2>/dev/null
killall -STOP "CommCenter" 2>/dev/null

echo "✅ NODO HIGIENIZADO: Flujo Laminar restaurado."
