#!/bin/bash
# 🏛️ OASIS INTELLIGENT SHIELD v2.0
export PYTHONPATH=$PYTHONPATH:~/Oasis-Sovereign-Monolith/core/lib

echo "🛡️ Escudo Inteligente Activo (κ=2.3). Analizando Manifold..."

while true; do
    LOAD=$(uptime | awk -F'load average:' '{ print $2 }' | cut -d, -f1 | tr -d ' ')
    
    # Usamos la lógica de tu paper para decidir
    python3 -c "from liboasis_math import calculate_informational_gravity; 
kappa, status = calculate_informational_gravity($LOAD, 1.0); 
if status == 'VISCOSO': exit(1)"
    
    if [ $? -eq 1 ]; then
        echo "⚠️ TURBULENCIA DETECTADA (KAPPA=$LOAD). Optimizando fase..."
        # En lugar de matar, armonizamos la prioridad
        sudo renice -n 10 -u oasis
    fi
    sleep 5
done
