#!/bin/zsh
# Desmontar si ya existe
for d in $(hdiutil info | awk '/\/dev\/disk[0-9]+/ {print $1}'); do
    if hdiutil info | grep -B 1 "ram://" | grep -q "$d"; then
        hdiutil detach "$d" -force 2>/dev/null || true
    fi
done
# Crear y montar 1 GB en HFS+
RAMDEV=$(hdiutil attach -nomount ram://2097152 | tr -d '[:space:]')
diskutil eraseVolume HFS+ "OasisRAM" "$RAMDEV" >/dev/null 2>&1
mkdir -p /Volumes/OasisRAM/tmp /Volumes/OasisRAM/models
chmod -R 777 /Volumes/OasisRAM
