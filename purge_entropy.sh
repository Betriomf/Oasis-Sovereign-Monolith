#!/bin/bash
echo "🌌 [OASIS PURGE]: Purgando entropía de memoria y procesos en macOS..."

# 1. Forzar la liberación de memoria RAM unificada (Caché inactiva)
sudo purge

# 2. Exterminar procesos zombis de telemetría y bloqueos de red
sudo killall -9 nc 2>/dev/null
sudo killall -9 com.adobe.GC.Invoker-1.0 2>/dev/null
sudo killall -9 com.google.keystone.agent 2>/dev/null
sudo killall -9 mdworker 2>/dev/null
sudo killall -9 mds 2>/dev/null
sudo killall suggestd newsd parsecd 2>/dev/null

# 3. Desactivar temporalmente la indexación Spotlight (elimina fricción de disco)
sudo mdutil -i off / > /dev/null 2>&1

# 4. Asignar prioridad máxima de tiempo real (-20) a Ollama
PID_OLLAMA=$(pgrep -f "ollama serve" | head -n 1)
if [ ! -z "$PID_OLLAMA" ]; then
    sudo renice -n -20 -p $PID_OLLAMA
    echo "⚡ [Prioridad]: Máxima prioridad reasignada a Ollama (PID: $PID_OLLAMA)"
fi

echo "✅ [Estado]: Memoria libre y silicio operando en régimen laminar frío."
