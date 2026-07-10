#!/bin/sh
echo "📦 Sellando investigaciones en el Monolito..."
git add .
git commit -m "🚀 Sincronización Soberana: $(date '+%Y-%m-%d %H:%M:%S') - Estado Laminar"
echo "📡 Transmitiendo a la Capa 0 (GitHub)..."
git push origin main
echo "✅ Sincronización completada. Investigaciones a salvo."
