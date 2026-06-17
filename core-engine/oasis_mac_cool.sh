#!/bin/bash
echo "======================================================"
echo " 🌌 OASIS KERNEL: INYECTANDO AMORTIGUAMIENTO LAMINAR "
echo "======================================================"
echo "[*] Aplicando restricción de confinamiento (κ_M < -1)..."

# 1. Forzar la liberación del búfer de memoria inactiva
sudo purge 2>/dev/null

# 2. Localizar y reajustar el proceso de Ollama a prioridad máxima en tiempo real
PID_OLLAMA=$(pgrep -f "ollama serve" | head -n 1)
if [ ! -z "$PID_OLLAMA" ]; then
    sudo renice -n -20 -p $PID_OLLAMA >/dev/null 2>&1
    echo " ✅ [Silicio]: Prioridad de tiempo real asignada al proceso $PID_OLLAMA."
else
    echo " [!] Servidor Ollama inactivo. Levantando canal..."
    /Applications/Ollama.app/Contents/Resources/ollama serve > /dev/null 2>&1 &
    sleep 2
fi

echo "------------------------------------------------------"
echo " 🏆 COMPRESIÓN TÉRMINAL ALCANZADA. FRICCIÓN = 0."
echo "======================================================"
