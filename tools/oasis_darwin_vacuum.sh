#!/bin/zsh
echo "🌌 [OASIS VACUUM]: Iniciando liberación de GB y ajuste de Kernel Darwin..."

# 1. Eliminar snapshots locales ocultos de APFS que consumen GB en silencio
for snap in $(tmutil listlocalsnapshotdates / 2>/dev/null | grep -E '^[0-9]{4}-'); do
    sudo tmutil deletelocalsnapshots "$snap" 2>/dev/null || true
done

# 2. Purgar cachés de paquetes, compilaciones y temporales de usuario
rm -rf ~/Library/Caches/pip ~/.cache ~/Library/Caches/Homebrew/downloads/* 2>/dev/null || true
sudo purge

# 3. Ajustar límites de descriptores de archivos (Dimensión 196883)
sudo sysctl -w kern.maxfiles=196883 >/dev/null
sudo sysctl -w kern.maxfilesperproc=196883 >/dev/null
ulimit -n 196883 2>/dev/null || true

# 4. Limpiar discos RAM huérfanos y asegurar el volumen /Volumes/OasisRAM
for d in $(hdiutil info | awk '/\/dev\/disk[0-9]+/ {print $1}'); do
    if hdiutil info | grep -B 1 "ram://" | grep -q "$d"; then
        hdiutil detach "$d" -force 2>/dev/null || true
    fi
done

RAMDEV=$(hdiutil attach -nomount ram://2097152 | tr -d '[:space:]')
diskutil eraseVolume HFS+ "OasisRAM" "$RAMDEV" >/dev/null 2>&1
mkdir -p /Volumes/OasisRAM/tmp /Volumes/OasisRAM/models
chmod -R 777 /Volumes/OasisRAM

echo "✅ [VACÍO COMPLETADO]: Espacio libre actual en SSD:"
df -h / | tail -n 1
