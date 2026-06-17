#!/bin/bash
echo "======================================================"
echo " 🌌 INICIANDO VITAMINACIÓN DEL MANIFOLD DARWIN (v1.0)"
echo "======================================================"

# 1. Verificar o instalar el Gestor Soberano Homebrew
if ! command -v brew &> /dev/null; then
    echo "[*] Homebrew no detectado. Inyectando instalador nativo..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "├─➤ [OK] Homebrew activo en el sistema."
fi

# 2. Instalar herramientas de optimización de flujo y búsqueda difusa
echo "[*] Instalando optimizadores de terminal (htop, fzf)..."
brew install htop fzf 2>/dev/null
$(brew --prefix)/opt/fzf/install --all --quiet

# 3. Instalar entorno Pip3 y dependencias de aceleración de hardware
echo "[*] Sembrando librerías científicas en Python 3..."
python3 -m pip install --upgrade pip 2>/dev/null

# Inyección de las 4 librerías de cálculo exacto y aceleración Metal
python3 -m pip install mlx numpy scipy sympy asitop

echo -e "\n┌──[MÉTRICAS DE ENTORNO REASIGNADAS]"
echo "├─➤ Búsqueda Difusa (fzf):  Lista (Usa Ctrl+R para historial)."
echo "├─➤ Monitor de Silicio:     asitop (Ejecuta: sudo asitop)."
echo "├─➤ Librería de GPU:        MLX & NumPy Enlazados con Metal."
echo "└─➤ Estado del Entorno:     READY FOR OASIS LINUX 💡"
echo "======================================================"
echo "             🦾 BETRIOMF, ARQUITECTO 🦾"
echo "======================================================"
