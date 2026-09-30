#!/bin/bash
echo "=================================================="
echo "🧹 PURGA MAESTRA DE ALMACENAMIENTO (macOS)"
echo "=================================================="

# 1. Eliminar snapshots locales de actualización de macOS (Recupera 5-10 GB)
echo "-> Purgando snapshots APFS locales..."
sudo tmutil deletelocalsnapshots 2289385E1A6FCCF05D444673FB1FEB06DDCF82A4C723EAD53AF1F3E08872CE0F 2>/dev/null || true
sudo tmutil deletelocalsnapshots MSUPrepareUpdate 2>/dev/null || true
for s in $(tmutil listlocalsnapshotdates / 2>/dev/null | grep -v "Snapshot"); do
    sudo tmutil deletelocalsnapshots "$s" 2>/dev/null || true
done

# 2. Purgar caché pesada de navegación y sistema
echo "-> Limpiando caché de Brave Browser..."
rm -rf ~/Library/Caches/BraveSoftware/Brave-Browser/Default/Cache/* 2>/dev/null
rm -rf ~/Library/Caches/BraveSoftware/Brave-Browser/Default/Code\ Cache/* 2>/dev/null

# 3. Purgar cachés de desarrollo y Homebrew
echo "-> Purgando cachés de Homebrew y herramientas..."
rm -rf ~/Library/Caches/Homebrew/* 2>/dev/null
brew cleanup --prune=all -s 2>/dev/null || true

# 4. Vaciar la papelera local
echo "-> Vaciando papelera..."
rm -rf ~/.Trash/* 2>/dev/null

# 5. Forzar sincronización del sistema de archivos
sync

echo "=================================================="
echo "✅ ESTADO ACTUAL DEL DISCO:"
df -h /
echo "=================================================="
