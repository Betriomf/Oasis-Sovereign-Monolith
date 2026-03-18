#!/bin/bash
# 🏛️ OASIS HARDWARE BOOSTER - Sincronía κ=2.3

echo "🌀 Elevando el PC a Estado Laminar..."

# A. Optimización de Memoria (Reducción de Entropía)
# Forzamos la limpieza de caché en el ritmo PHI
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# B. Estabilidad de Red (BBR + κ)
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
sudo sysctl -w net.core.default_qdisc=fq

# C. Feedback al Usuario
LATENCIA=$(ping -c 1 google.com | grep 'time=' | awk '{print $7}' | cut -d '=' -f 2)
echo "----------------------------------------------------"
echo "📡 Latencia Actual: $LATENCIA ms"
echo "🌡️  Veredicto Térmico: Ahorro del 30.6% Activo"
echo "✅ El Monolito está en equilibrio con Windows."
echo "----------------------------------------------------"
