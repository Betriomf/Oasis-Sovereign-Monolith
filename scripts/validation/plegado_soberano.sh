#!/bin/bash
# 🏛️ OASIS SOVEREIGN: AUTOMATED DATA FOLDING
# Basado en la Constante kappa = 2.3

VAULT="/mnt/c/Users/Mariano/Documents/Oasis_Vault"
SOURCE_DIR="$HOME/Oasis-Sovereign-Monolith"
DATE=$(date +%Y%m%d)

echo "░▒▓ INICIANDO PLEGADO TERMODINÁMICO ▓▒░"

# 1. Comprobar si existe el Búnker
if [ ! -d "$VAULT" ]; then
    echo "⚠️ Error: El Búnker en Windows no existe. Creándolo..."
    mkdir -p "$VAULT"
fi

# 2. Plegar archivos y mover al Búnker (LZ4 - Ratio 2.3 friendly)
echo "> Plegando bitstream de Oasis..."
tar -I 'lz4 -9' -cvf "$VAULT/Oasis_Archive_$DATE.tar.lz4" "$SOURCE_DIR" --exclude="*.lz4"

# 3. Verificación de Gravedad
echo "------------------------------------------------"
du -h "$VAULT/Oasis_Archive_$DATE.tar.lz4"
echo "✅ Plegado completado. Datos seguros en el Búnker de Windows."
