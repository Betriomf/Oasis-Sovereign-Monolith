#!/bin/bash
PARASITOS=("suggestd" "cloudpairingd" "cloudd" "remotemanagementd")
echo "🌌 OASIS MAC-SENTINEL: PURGANDO ENTROPÍA APPLE..."
for p in "${PARASITOS[@]}"; do
    if pgrep -x "$p" > /dev/null; then
        killall -9 "$p" 2>/dev/null
        echo "✅ PURGA: $p eliminado."
    fi
done
echo "💹 ESTADO: Eficiencia Landauer Recuperada."
