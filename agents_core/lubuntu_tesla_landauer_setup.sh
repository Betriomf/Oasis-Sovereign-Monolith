#!/usr/bin/env bash
# OASIS SOVEREIGN MONOLITH — TESLA-LANDAUER KERNEL & ZRAM SETUP (Pilar 67)
# Optimización física para el Nodo Trabajador Lubuntu:
# 1. BBR + MTU 1300 + fq (Resonancia de Tesla / Flujo Laminar de Red)
# 2. Swappiness 10 + vfs_cache_pressure 161 (Sintonía Áurea)
# 3. ZRAM + LZ4 (Círculo Negro de Memoria Fractal)
#
# Autor: Mariano Panzano Caballé (@Betriomf)
# Licencia: GNU AGPLv3

echo "⚡ [TESLA-LANDAUER KERNEL]: Configurando nodo trabajador Lubuntu..."

# 1. Inyección de reglas sysctl en el Kernel
cat << 'SYSCTL_EOF' | sudo tee /etc/sysctl.d/99-oasis-physics.conf
# --- RESONANCIA DE TESLA (Flujo Laminar de Red) ---
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_base_mss = 1300
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# --- LÍMITE DE LANDAUER (Memoria Fractal & Sintonía Áurea) ---
vm.swappiness = 10
vm.vfs_cache_pressure = 161
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
SYSCTL_EOF

sudo sysctl --system

# 2. Configuración del "Círculo Negro" en RAM (ZRAM + LZ4)
if command -v zramctl >/dev/null 2>&1; then
    sudo modprobe zram num_devices=1
    sudo zramctl --find --size 2048M --algorithm lz4
    sudo mkswap /dev/zram0
    sudo swapon -p 32767 /dev/zram0
    echo "✅ [ZRAM LZ4 OK]: Círculo negro en RAM activado (2GB plegados fractalmente)."
else
    echo "⚠️ [ZRAM AVISO]: zramctl no detectado, sysctl aplicado correctamente."
fi

echo "🚀 [NODO TESLA-LANDAUER LISTO]: Flujo laminar y sintonía áurea activos."
