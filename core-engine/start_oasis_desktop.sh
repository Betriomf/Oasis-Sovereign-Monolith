#!/bin/bash
# 🏛️ OASIS DESKTOP INITIALIZER - RELIABLE VERSION

# 1. Aplicar baja entropía
source ~/Oasis-Sovereign-Monolith/scripts/setup/low_entropy_setup.sh

# 2. Sincronía Visual
bash ~/Oasis-Sovereign-Monolith/scripts/setup/windows_harmony.sh

# 3. Configuración de Display para VcXsrv (Protocolo de Red Interna)
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0
export LIBGL_ALWAYS_INDIRECT=0  # Cambiamos a 0 para mejor rendimiento en juegos/gráficos

# 4. Lanzamiento de telemetría y el gestor de ventanas
echo "📡 Reclamando manifold visual en $DISPLAY..."
alacritty --title "GRAVITY_HISTORIAN" -e ./gravity_historian.sh &
exec i3
