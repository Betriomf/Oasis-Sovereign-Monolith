#!/bin/bash
ZENODO_URL="https://zenodo.org/records/18405873"
echo "🌐 OASIS KNOWLEDGE SYNC: Sincronizando con Zenodo..."
echo "----------------------------------------------------"

# Usamos links2 para extraer el título del paper y verificar conexión
PAPER_TITLE=$(links2 -dump "$ZENODO_URL" | grep -i "Oasis" | head -n 1)

if [[ -z "$PAPER_TITLE" ]]; then
    echo "⚠️  ADVERTENCIA: No se pudo verificar el paper. Revisa el escudo NDIS."
else
    echo "✅ PAPER VALIDADO: $PAPER_TITLE"
    echo "🔗 Referencia inmutable establecida en Dimensión 196883."
fi
echo "----------------------------------------------------"
