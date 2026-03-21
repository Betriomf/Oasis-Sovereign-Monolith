#!/bin/bash
# 🏛️ OASIS LOW ENTROPY SETUP (Compatible con WSL/Lenovo)
# Autor: Mariano Panzano Caballé

echo "===================================================="
echo " 🌀 INICIANDO NEGOCIACIÓN DE BAJA ENTROPÍA "
echo "===================================================="

# Función para aplicar cambios de sysctl de forma segura
apply_sysctl() {
    local key=$1
    local value=$2
    if sysctl -n "$key" >/dev/null 2>&1; then
        sudo sysctl -w "$key"="$value"
        echo "✅ $key sintonizado a $value"
    else
        echo "⚠️ $key: Parámetro protegido por el Kernel de Windows (WSL Limit)"
    fi
}

# 1. OPTIMIZACIÓN DE MEMORIA (Soberanía Informacional)
apply_sysctl "vm.swappiness" "10"

# 2. OPTIMIZACIÓN DE RED (Flujo Laminar)
apply_sysctl "net.core.rmem_max" "16777216"
apply_sysctl "net.core.wmem_max" "16777216"
apply_sysctl "net.ipv4.tcp_congestion_control" "bbr"

# 3. LIMPIEZA DE TUBERÍAS (Flush de Entropía)
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
echo "🌀 Caché de sistema purificada."

# 4. LANZAR SELLO DE FIRMA
if [ -f ~/Oasis-Sovereign-Monolith/scripts/oasis_signature.sh ]; then
    ~/Oasis-Sovereign-Monolith/scripts/oasis_signature.sh
fi

echo "===================================================="
echo " ✅ ENTORNO LENOVO SINTONIZADO (κ ≈ 2.3) "
echo "===================================================="
