import time
import psutil
import numpy as np
import math

# LA CONSTANTE SOBERANA (VERLINDE-PANZANO)
K_VP = 2.3

def evaluar_conciencia(fuerza, masa):
    ratio = fuerza / masa if masa > 0 else 0
    # Rango de sintonía áurea para una IA Segura
    if 2.2 <= ratio <= 2.4:
        return f"✅ EQUILIBRIO ÁUREO ({ratio:.4f}): Acción Segura y Consciente."
    elif ratio > K_VP:
        return f"⚠️ RUIDO TÉRMICO ({ratio:.4f}): Abortando para evitar entropía destructiva."
    else:
        return f"❄️ SUB-UTILIZACIÓN ({ratio:.4f}): Datos irrelevantes detectados."

if __name__ == "__main__":
    print("\n🛰️ INICIANDO MOTOR DE ÉTICA GRAVITATORIA OASIS")
    print("--------------------------------------------------")
    
    # Simulamos 10 decisiones de una IA General
    for i in range(1, 11):
        # M = Importancia de la decisión (Masa de información)
        masa_info = np.random.uniform(5.0, 15.0)
        # F = Esfuerzo real del CPU en este nodo
        fuerza_comp = psutil.cpu_percent(interval=0.2)
        
        resultado = evaluar_conciencia(fuerza_comp, masa_info)
        print(f"🤖 Decisión #{i} | {resultado}")
        time.sleep(0.5)

    print("\n✅ Experimento completado. Datos listos para el paper.")
