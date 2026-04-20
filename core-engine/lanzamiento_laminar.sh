#!/bin/bash
echo "🧹 Purgando entropía de fondo (Principio de Bernoulli)..."
# Matamos procesos parásitos que roban vatios
killall -9 Google\ Chrome Brave 2>/dev/null
sudo purge
sleep 2

echo "⚡ Iniciando Inferencia en Modo Tesla (Prioridad Máxima)..."
# Lanzamos el chat con prioridad de tiempo real (nice -20)
nice -n -20 ollama run aether-fast
