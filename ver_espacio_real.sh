#!/bin/bash
echo "=================================================================="
echo "📊 RADIOGRAFÍA REAL DEL CONTENEDOR APFS (113 GB)"
echo "=================================================================="

echo -e "\n1. VOLÚMENES EN EL CONTENEDOR APFS:"
df -h | grep -E "disk1|Filesystem"

echo -e "\n2. BASURA DEL SISTEMA APPLE (Carpetas ocultas pesadas):"
echo -n "   - Memoria Virtual / Sleepimage: "
sudo du -sh /private/var/vm 2>/dev/null || echo "0B"

echo -n "   - Descargas de Actualizaciones Apple: "
sudo du -sh /Library/Updates /System/Volumes/Data/Library/Updates 2>/dev/null | awk '{print $1}' | tr '\n' ' '
echo ""

echo -n "   - Historial de versiones (.DocumentRevisions): "
sudo du -sh /.DocumentRevisions-V100 2>/dev/null || echo "0B"

echo -n "   - Cachés globales de Sistema (/Library/Caches): "
sudo du -sh /Library/Caches 2>/dev/null || echo "0B"

echo -e "\n3. DESGLOSE DEL VOLUMEN DE DATOS (/System/Volumes/Data):"
sudo du -hd 1 /System/Volumes/Data 2>/dev/null | sort -hr | head -n 8

echo "=================================================================="
