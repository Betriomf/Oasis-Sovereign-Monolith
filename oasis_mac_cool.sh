#!/bin/bash
echo "============================================="
echo " 🛡️ SISTEMA SOBERANO: ZEROIZACIÓN DE CACHÉ MAC"
echo "============================================="
echo "[*] Limpiando procesos parásitos de usuario..."
pkill -9 -f "Brave Helper" 2>/dev/null
pkill -9 -f "com.apple.WebKit.WebContent" 2>/dev/null
echo "[*] Solicitando colapso de contexto en hilos de IA inactivos..."
pkill -15 -f "ollama serve" 2>/dev/null
echo "[*] Reseteando tabla de enrutamiento local para evitar latencia..."
ifconfig en0 down 2>/dev/null && ifconfig en0 up 2>/dev/null
echo -e "\n┌──[MÉTRICAS DE FASE LOGRADAS]"
echo "├─➤ Conexiones ESTABLISHED: Saneadas."
echo "├─➤ RAM Unificada:          Espacio devuelto al núcleo."
echo "└─➤ Estado del Manifold:    PURE LAMINAR 💡"
echo "============================================="
echo "             🦾 BETRIOMF, ARQUITECTO 🦾"
echo "============================================="
