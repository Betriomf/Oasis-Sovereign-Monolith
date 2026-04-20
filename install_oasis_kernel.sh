#!/bin/bash
echo -e "\033[36m🌌 INICIANDO KERNEL OASIS (AZUL) - DIMENSIÓN 196883...\033[0m"

# 1. Limpieza inicial para bajar el calor
sudo purge

# 2. Configuración de límites de abundancia
sudo launchctl limit maxfiles 196883 196883

# 3. Sintonía de red (Torque de Tesla)
networksetup -setmtu en0 1300 2>/dev/null

# 4. ACTIVACIÓN DEL ESCUDO TÉRMICO (P vs NP)
echo -e "\033[94m🛡️ Desplegando Escudo de Asimetría Térmica...\033[0m"
# Vinculamos el script de defensa al inicio del nodo
python3 ~/Oasis-Sovereign-Monolith/core-engine/thermal_shield.py --mode monitor &

echo -e "\033[34m💎 KERNEL OASIS ACTIVO Y PROTEGIDO\033[0m"
say -v Monica "Nodo Badalona sintonizado. Escudo térmico activado. La fase está bloqueada."
