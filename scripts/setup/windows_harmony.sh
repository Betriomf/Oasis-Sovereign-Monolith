#!/bin/bash
echo "🌀 Sincronizando armonía visual con el host..."
powershell.exe -Command "Stop-Process -Name explorer -Force; Start-Process explorer"
echo "✅ Interfaz de Windows refrescada y alineada con κ=2.3"
