#!/bin/bash
echo "🧹 [Oasis Disk Liberator]: Iniciando limpieza profunda..."

echo "-> Limpiando caché de Homebrew..."
brew cleanup --prune=all -s 2>/dev/null
rm -rf ~/Library/Caches/Homebrew/* 2>/dev/null

echo "-> Purgando cachés de pip y Python..."
pip cache purge 2>/dev/null
find ~ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "-> Purgando cachés de usuario no críticas..."
rm -rf ~/Library/Caches/BraveSoftware/Brave-Browser/Default/Cache/* 2>/dev/null
rm -rf ~/Library/Caches/com.apple.coresymbolicationd 2>/dev/null

echo "-> Limpiando target de Rust en el Monolito..."
if [ -d "$HOME/Oasis-Sovereign-Monolith/apps/desktop" ]; then
    (cd "$HOME/Oasis-Sovereign-Monolith/apps/desktop" && cargo clean 2>/dev/null || true)
fi

echo "✅ Limpieza completada. Nuevo estado del disco:"
df -h /
