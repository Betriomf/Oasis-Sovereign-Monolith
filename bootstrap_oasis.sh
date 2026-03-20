#!/bin/bash
# 🏛️ OASIS OS BOOTSTRAPPER
echo "🚀 Instalando Oasis Sovereign OS Layer..."

# 1. Instalación de dependencias de ciencia
sudo apt update && sudo apt install -y bc htop stress-ng python3-numpy

# 2. Configuración del Manifest de Interfaz (El que optimiza Windows/Lenovo)
source ./scripts/setup/oasis_ui_manifest.sh

# 3. Lanzar el Historiador de Gravedad en segundo plano
./core-engine/gravity_historian.sh &

echo "✅ Sistema Oasis OS instalado y fluyendo como el agua."
