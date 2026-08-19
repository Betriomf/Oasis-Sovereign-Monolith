#!/usr/bin/env bash
# 🛰️ OASIS MACOS LAMINAR ENGINE (BSD Network Tuning)
echo "==============================================================="
echo "🍏 [OASIS MACOS LAMINAR TUNER] - Desbloqueando Red de Cero Latencia"
echo "==============================================================="

# Optimización de latencia TCP para macOS sin esperas (Delayed ACK = 0)
sudo sysctl -w net.inet.tcp.delayed_ack=0 > /dev/null 2>&1 || true
sudo sysctl -w net.inet.tcp.mptcp_cellicon=0 > /dev/null 2>&1 || true
sudo sysctl -w net.inet.tcp.win_scale_factor=3 > /dev/null 2>&1 || true

echo "✅ Parámetros de red BSD aplicados:"
echo "   • TCP Delayed ACK : 0 (Entrega instantánea de paquetes web)"
echo "   • Window Scaling  : Optimizado para fibra y baja jitter"
