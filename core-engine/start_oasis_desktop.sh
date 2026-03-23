#!/bin/bash
# 🏛️ OASIS DESKTOP - PHASE-LOCKING SUPPRESSION (κ=2.3)

# 1. Sintonização de Baixa Entropia
source ~/Oasis-Sovereign-Monolith/scripts/setup/low_entropy_setup.sh

# 2. LIMPEZA DE COLISÕES (Evita o erro "WM_Sn is owned")
echo "🧹 Purificando manifold visual..."
killall i3 2>/dev/null

# 3. Configuração de Túnel Direto
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0

# 4. Injeção da Livraria Oasis (Trigonometria de Fase)
export PYTHONPATH=$PYTHONPATH:~/Oasis-Sovereign-Monolith/core/lib
python3 -c "from liboasis_math import calculate_informational_gravity; print('✅ Sincronia:', calculate_informational_gravity(10, 5))"

echo "🌀 Reclamando Manifold Visual (Modo Soberano)..."

# 5. Lançamento com Supressão de Erros de Handshake
# Tentamos o i3; se falhar, lançamos o terminal Alacritty direto
(i3 --replace) || (alacritty --title "OASIS_EMERGENCY_NODE")
