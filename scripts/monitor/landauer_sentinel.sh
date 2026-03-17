#!/bin/bash
SINGULARITIES=("CompatTelRunner.exe" "SettingSyncHost.exe" "CloudExperienceHost.exe")
echo "🌌 OASIS LANDAUER SENTINEL: PURGANDO ENTROPÍA..."
for ghost in "${SINGULARITIES[@]}"; do
    if tasklist.exe /FI "IMAGENAME eq $ghost" 2>nul | grep -q "$ghost"; then
        taskkill.exe /F /IM "$ghost" /T >nul 2>&1
        echo "✅ PURGA: $ghost eliminado."
    fi
done
