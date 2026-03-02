#!/bin/bash
# 🏛️ OASIS PHI-SCHEDULER CORE
PHI=$(echo "scale=10; (sqrt(5)-1)/2" | bc -l)
BASE_MS=1000
NODE_ID=$(hostname | cksum | cut -d' ' -f1)
OFFSET=$(echo "$NODE_ID * $PHI" | bc -l | awk '{print $1 % 1}')

echo "===================================================="
echo "  OASIS SOVEREIGN NODE: GEOMETRIC RECOVERY ACTIVE"
echo "===================================================="
for k in {1..5}
do
    PHASE=$(echo "$OFFSET + $k * $PHI" | bc -l | awk '{print $1 % 1}')
    DELAY=$(echo "$BASE_MS * $PHASE" | bc -l | cut -d. -f1)
    echo "⚡ Step $k | Phase: $PHASE | Delay: ${DELAY}ms"
    sleep $(echo "scale=3; $DELAY/1000" | bc -l)
done
echo "✅ Handshake Successful."
