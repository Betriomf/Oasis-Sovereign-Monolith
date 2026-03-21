#!/bin/bash
# 🏛️ OASIS DESKTOP INITIALIZER

# 1. Aplicar baja entropía al sistema antes de abrir ventanas
source ~/Oasis-Sovereign-Monolith/scripts/setup/low_entropy_setup.sh

# 2. Lanzar el Historiador de Gravedad en una ventana flotante
alacritty -e ./gravity_historian.sh &

# 3. Lanzar el Compositor de Ventanas con limitación de fase Φ
# Picom gestiona las sombras y transparencias de forma laminar
picom --backend glx --vsync --refresh-rate 60 &

# 4. Iniciar el gestor de ventanas
exec i3
