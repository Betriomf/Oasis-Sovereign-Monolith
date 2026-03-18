#!/bin/bash
ARCHIVO=$1
if [ -f "$ARCHIVO" ]; then
    echo "🔐 CIFRANDO: Protegiendo $ARCHIVO con Grado Militar..."
    gpg --symmetric --batch --passphrase "Oasis2.3" "$ARCHIVO"
    echo "✅ $ARCHIVO.gpg creado. El original puede ser purgado."
else
    echo "❌ Error: Especifica un archivo válido de Betriomf."
fi
