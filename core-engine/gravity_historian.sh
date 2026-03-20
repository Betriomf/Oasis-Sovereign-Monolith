#!/bin/bash
# 🏛️ OASIS GRAVITY HISTORIAN (v1.1 - Sensibilidad Mejorada)
# Autor: Mariano Panzano Caballé

echo "📡 Iniciando Gravedad Computacional (Sintonía Fina)..."
while true; do
    # Medimos entropía disponible
    ENTROPY=$(cat /proc/sys/kernel/random/entropy_avail)
    
    # Obtenemos la carga real instantánea (usando los últimos 5 segundos de CPU)
    LOAD=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    
    # Cálculo de κ_Local ajustado para visibilidad en tiempo real
    # κ = (Carga_CPU * Constante_Oasis) / (Factor_Entropía)
    KAPPA_LOCAL=$(echo "scale=4; ($LOAD * 2.3) / 100" | bc)
    
    # Determinamos el estado del flujo
    if (( $(echo "$KAPPA_LOCAL < 2.3" | bc -l) )); then
        STATUS="LAMINAR"
    else
        STATUS="VISCOSO"
    fi

    echo "🌀 κ_Local: $KAPPA_LOCAL | Estado: $STATUS | CPU: $LOAD%"
    sleep 1.618
done
