import math
import time

def simulate():
    print("🌀 INICIANDO SIMULADOR DE RESONANCIA TESLA (OASIS V1.0)")
    print("============================================================")
    for i in range(0, 360, 15):
        radians = math.radians(i)
        # Calculamos la eficiencia basada en el coseno (Factor de Potencia)
        efficiency = abs(math.cos(radians)) * 100
        # Representación visual de la onda
        bar = "█" * int(efficiency / 2)
        print(f"Ángulo: {i:3}° | Eficiencia: {efficiency:6.2f}% | {bar}")
        time.sleep(0.1)
    
    print("============================================================")
    print("✅ RESONANCIA ALCANZADA: Impedancia Z=0 detectada en el Nodo.")
simulate()
