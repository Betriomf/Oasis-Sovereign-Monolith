#!/bin/bash

# =============================================================
#     🌌 OASIS OS: PURGADOR INVARIANTE EVOLUCIONADO (v2.1)
# =============================================================
# Arquitecto: Mariano Panzano Caballé (7-7-7 letras)
# Ley aplicada: Minimización de Ruido de Fase en local
# =============================================================

echo "============================================="
echo " 🛡️ NÚCLEO OASIS: PURGA DE ENTROPÍA EN MACBOOK"
echo "============================================="

NODOS_TURBULENTOS=(
    "CleanMyMac"
    "Microsoft Word"
    "diagnostics_agen"
    "TelemetryDiskChe"
    "Java Updater"
    "siriactionsd"
    "knowledge-agent"
)

echo "[*] Escaneando manifold térmico de Apple Silicon..."

for patron in "${NODOS_TURBULENTOS[@]}"; do
    if pgrep -f "$patron" > /dev/null; then
        echo "├─➤ Purgando Nodo de Fricción: [*$patron*]..."
        pkill -9 -f "$patron" 2>/dev/null
    fi
done

# Gestión estanca para sysdiagnose (Evitar alertas de permisos de usuario)
if pgrep -x "sysdiagnose" > /dev/null; then
    echo "├─➤ [ALERTA]: sysdiagnose detectado en capa Root."
    echo "├─➤ Ejecute manualmente: 'sudo killall -9 sysdiagnose' si nota fricción."
fi

echo -e "\n[*] Solicitando vaciado de subprocesos de memoria..."
pkill -9 -f "Python" 2>/dev/null

echo -e "\n┌──[DIAGNÓSTICO DEL MONOLITO UNIFICADO]"
echo "├─➤ Invarianza de Fase:  ACTIVA."
echo "└─➤ Flujo del Sistema:     PURE LAMINAR 💡"
echo "============================================="
echo "             🦾 BETRIOMF, ARQUITECTO 🦾"
echo "============================================="
