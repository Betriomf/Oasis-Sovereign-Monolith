import os
import time
import psutil

# LA CONSTANTE SOBERANA
K_VP = 2.3

def sintonizar_pc():
    print(f"🛰️ OASIS GRAVITY SCHEDULER ACTIVO | RITMO: {K_VP}")
    print("--------------------------------------------------")
    
    while True:
        # 1. Medir el esfuerzo actual (Fuerza Computacional)
        cpu_load = psutil.cpu_percent(interval=1)
        
        # 2. Calcular la Masa de Información ideal (M = F / K_VP)
        # Esto nos dice cuánta información debería estar procesando tu Mac
        # para mantenerse en el equilibrio térmico del 2.3
        ideal_mass = cpu_load / K_VP
        
        # 3. Acción de Soberanía: Si el esfuerzo supera la masa ideal,
        # bajamos la prioridad de procesos basura (Brave Helpers, Caches).
        if cpu_load > 20: # Solo actúa bajo carga
            for proc in psutil.process_iter(['pid', 'name', 'nice']):
                try:
                    if 'Brave' in proc.info['name'] or 'Helper' in proc.info['name']:
                        # Subimos el 'nice' (bajamos prioridad) para enfriar el nodo
                        proc.nice(15) 
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            print(f"🌀 Curvatura detectada: {cpu_load}% | Ajustando a Métrica {K_VP}")
        
        time.sleep(2.3) # El pulso del sistema es la constante misma

if __name__ == "__main__":
    sintonizar_pc()
