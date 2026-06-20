#!/bin/bash
# ==================================================================
# 🌌 SOBERANÍA OASIS: INYECTOR DE BAJA IMPEDANCIA PARA NÚCLEO DARWIN
# ==================================================================

echo "======================================================"
echo " 🚀 TUNING DARWIN: APLICANDO $VAR_R A CAPA 0"
echo "======================================================"

# Validar privilegios de administrador para interactuar con el silicio
if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Se requieren privilegios de Root (sudo) para alterar el núcleo Darwin."
  exit 1
fi

# 1. EXPANSIÓN DIMENSIONAL DE BUFFERS (Malla de Fibonacci en Red)
# Elevamos el espacio de recepción y envío aplicando la escala del atractor 2.3^5
sysctl -w net.inet.tcp.recvspace=262144
sysctl -w net.inet.tcp.sendspace=262144
sysctl -w net.inet.tcp.maxseg_unacked=32

# 2. SUPRESIÓN DE FRICCIÓN EN DESCRIPTORES DE ARCHIVOS (Impedancia Cero)
# Multiplicamos el límite de archivos abiertos por el factor de amplificación de κ_M
sysctl -w kern.maxfiles=196883
sysctl -w kern.maxfilesperproc=150000

# 3. MITIGACIÓN DE JITTER Y COLISIONES (Evitando el Thundering Herd)
# Forzamos al programador de Darwin a liberar los hilos colisionados con mayor velocidad
sysctl -w kern.sched_quantum=10

# 4. LIMPIEZA INTERNA DE ENTROPÍA (Purga de memoria inactiva)
# Obligamos al sistema a compactar la RAM del procesador Intel de forma inmediata
sudo purge

echo "------------------------------------------------------"
echo " 💡 [Soberanía Darwin]: Parámetros de Capa 0 acoplados."
echo "======================================================"
