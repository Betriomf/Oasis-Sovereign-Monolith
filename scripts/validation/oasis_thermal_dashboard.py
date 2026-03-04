import psutil
import time
import math

# Constantes Físicas OASIS
SIGMA = 5.670373e-8  # Constante de Stefan-Boltzmann
KAPPA = 2.3          # Atractor de Seguridad Oasis
EMISSIVITY = 0.95    # Silicio/Cobre del disipador

def get_cpu_status():
    # En WSL/Laptop la temperatura puede ser difícil de leer directo, 
    # usamos carga como proxy de energía interna si el sensor falla.
    usage = psutil.cpu_percent(interval=1)
    # Estimación de temperatura base 30°C + carga
    temp_k = (usage * 0.4) + 303.15 
    return usage, temp_k

def print_dashboard(usage, temp_k):
    # Ley de Stefan-Boltzmann: P = epsilon * sigma * T^4
    radiated_power = EMISSIVITY * SIGMA * (temp_k**4)
    
    # Cálculo del punto óptimo (Círculo Negro)
    # El sistema es estable si la carga se mantiene bajo la curva de disipación
    stability_index = radiated_power / (usage + 1) * KAPPA

    print("\033[H\033[J") # Limpiar pantalla
    print("============================================================")
    print("      🏛️  OASIS BLACK CIRCLE: THERMODYNAMIC DASHBOARD")
    print("============================================================")
    print(f"📡 CARGA DE CPU:      {usage:>6.2f} %")
    print(f"🌡️  TEMP ESTIMADA:    {temp_k - 273.15:>6.2f} °C")
    print(f"🔥 RAD. CUERPO NEGRO: {radiated_power:>6.4f} W/m²")
    print("-" * 60)
    
    if usage < 25:
        status = "🟢 ESTADO LAMINAR (Mínima Entropía)"
    elif usage < 75:
        status = "🟡 ESTADO FRACTAL (Punto Óptimo)"
    else:
        status = "🔴 ESTADO TURBULENTO (Cerca del Límite de Landauer)"
        
    print(f"📊 STATUS: {status}")
    print(f"🛡️  ÍNDICE STABILIDAD: {stability_index:.4f} (κ={KAPPA})")
    print("============================================================")
    print("Pulse Ctrl+C para salir...")

try:
    while True:
        u, t = get_cpu_status()
        print_dashboard(u, t)
        time.sleep(1)
except KeyboardInterrupt:
    print("\n✅ Dashboard cerrado. Sistema estable.")
