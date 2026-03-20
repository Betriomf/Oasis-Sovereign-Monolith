#!/bin/bash
# 🏛️ OASIS LOW ENTROPY SETUP
echo "🌀 Minimizando entropía del Sistema Operativo..."
# Evita el uso de disco lento y ajusta buffers
sudo sysctl -w vm.swappiness=10
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216
# Sello de autoría
~/Oasis-Sovereign-Monolith/scripts/oasis_signature.sh
echo "✅ Windows/Linux en Armonía κ=2.3."
