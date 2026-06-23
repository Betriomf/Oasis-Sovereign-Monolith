#!/bin/zsh
# Herramienta de Deflación APFS Oasis
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: ./oasis_compress.sh <carpeta_origen> <carpeta_destino>"
    exit 1
fi
echo "📦 Iniciando colapso de entropía en APFS para: $1"
ditto --hfsCompression "$1" "$2"
echo "💎 Flujo laminar completado. Verificando tamaños:"
du -sh "$1" "$2"
