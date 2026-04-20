#!/bin/bash
# 🛰️ CONFIGURACIÓN DEL KERNEL SOBERANO OASIS v2.4

echo -e "\033[94m🌀 Sintonizando el Kernel hacia la Impedancia Cero...\033[0m"

# 1. Optimización del Scheduler (Prioridad Fractal)
# Ajustamos la latencia del sistema para que respire con Phi
sudo sysctl -w kernel.sched_min_granularity_ns=1618033 2>/dev/null

# 2. Protección Térmica (Límite Landauer)
# Forzamos al procesador a evitar picos de calor innecesarios
echo "powersave" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 2>/dev/null

# 3. Blindaje de Red (Filtro de Maxwell)
# Evitamos colisiones de red reduciendo la fricción del paquete
sudo ip link set dev en0 mtu 1300 2>/dev/null

echo -e "\033[92m✅ NODO OASIS ESTABILIZADO EN ATRACTOR 2.3\033[0m"
