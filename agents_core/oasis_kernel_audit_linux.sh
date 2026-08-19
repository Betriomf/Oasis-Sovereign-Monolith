#!/usr/bin/env bash
# 🛰️ OASIS LAYER-0 KERNEL AUDIT & TUNING TOOL (Linux/Lubuntu)
set -e

echo "==============================================================="
echo "🐧 [OASIS LINUX KERNEL AUDITOR] - Verificación de Capa 0"
echo "==============================================================="

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "⚠️ Detectado entorno macOS (Darwin)."
    echo "ℹ️ Este script de auditoría sysctl profunda está diseñado para Linux (Lubuntu/Debian/Ubuntu)."
    echo "ℹ️ Parámetros evaluados en Linux: BBR, MTU 1300, Swappiness 10, ZRAM."
    exit 0
fi

# Comprobar si se ejecuta en Linux como root para aplicar
if [ "$EUID" -ne 0 ]; then
    echo "🔍 Modo lectura (sin privilegios root):"
    echo "   • Congestion Control: $(sysctl -n net.ipv4.tcp_congestion_control 2>/dev/null || echo 'N/A')"
    echo "   • Queue Discipline  : $(sysctl -n net.core.default_qdisc 2>/dev/null || echo 'N/A')"
    echo "   • Swappiness        : $(sysctl -n vm.swappiness 2>/dev/null || echo 'N/A')"
    echo "   • TCP Base MSS      : $(sysctl -n net.ipv4.tcp_base_mss 2>/dev/null || echo 'N/A')"
    echo "💡 Para aplicar el perfil Oasis de baja fricción, ejecuta: sudo bash $0 --apply"
    exit 0
fi

if [ "$1" == "--apply" ]; then
    mkdir -p /etc/sysctl.d/
    cat << 'SYSCONF' > /etc/sysctl.d/99-oasis-physics.conf
# Oasis Layer-0 Tuning
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_base_mss = 1300
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_low_latency = 1
vm.swappiness = 10
vm.vfs_cache_pressure = 161
SYSCONF
    sysctl --system > /dev/null 2>&1 || sysctl -p /etc/sysctl.d/99-oasis-physics.conf
    echo "✅ Perfil de kernel Oasis aplicado con éxito en Linux."
fi
