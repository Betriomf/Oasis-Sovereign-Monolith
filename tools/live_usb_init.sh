#!/bin/busybox sh
# ==============================================================================
# OASIS SOVEREIGN OS — LIVE-USB INITRAMFS BOOTSTRAP (Pilar 364)
# Arranque autónomo en silicio frío sin disco duro ni conexión a internet.
# ==============================================================================

# 1. Montaje de sistemas de archivos virtuales del núcleo
/bin/busybox mount -t proc proc /proc
/bin/busybox mount -t sysfs sysfs /sys
/bin/busybox mount -t devtmpfs devtmpfs /dev

echo "🛰️ [OASIS SOVEREIGN BOOT]: Iniciando hardware en régimen de silicio frío..."

# 2. Vacío Computacional: disco RAM volátil (Zero SSD/Flash wear)
mkdir -p /tmp/oasis_vacuum
/bin/busybox mount -t tmpfs -o size=512M,noatime,nodev,nosuid tmpfs /tmp/oasis_vacuum

# 3. Montar partición persistente del USB en /workspace (si existe)
mkdir -p /workspace
USB_DATA_DEV=$(/bin/busybox blkid | grep 'LABEL="OASIS_DATA"' | cut -d: -f1)
if [ -n "$USB_DATA_DEV" ]; then
    /bin/busybox mount -o noatime "$USB_DATA_DEV" /workspace
    echo "💾 [LIVE-USB]: Partición persistente OASIS_DATA montada en /workspace."
else
    /bin/busybox mount -t tmpfs tmpfs /workspace
    echo "⚠️ [LIVE-USB]: Modo volátil puro en RAM (sin almacenamiento persistente)."
fi

# 4. Configurar red link-local (Ad-Hoc / Ethernet / Wi-Fi)
/bin/busybox ifconfig lo 127.0.0.1 up
/bin/busybox ifconfig eth0 up 2>/dev/null || true

# 5. Iniciar Gateway de Oasis (el mismo núcleo que en Render)
export PORT=8080
export VACUUM_DIR=/tmp/oasis_vacuum
if [ -f /usr/bin/python3 ]; then
    echo "⚡ [LIVE-USB]: Lanzando Gateway Soberano v10.0 en http://127.0.0.1:8080/terminal"
    python3 /agents_core/oasis_render_gateway.py > /tmp/oasis_vacuum/gateway.log 2>&1 &
fi

# 6. Lanzar shell de consola BusyBox interactiva
exec /bin/busybox sh
