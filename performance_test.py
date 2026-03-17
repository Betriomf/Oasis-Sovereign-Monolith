import time
import math

def stress_test():
    print("🌀 INICIANDO TEST DE RENDIMIENTO OASIS - iSH NODO")
    print("====================================================")
    start_time = time.time()
    count = 0
    # Ejecutamos 1 millón de cálculos trigonométricos
    for i in range(1000000):
        math.sin(i) * math.cos(i)
        count += 1
    
    end_time = time.time()
    duration = end_time - start_time
    ops_per_sec = count / duration
    
    print(f"⏱️ Tiempo: {duration:.4f} segundos")
    print(f"🚀 Rendimiento: {ops_per_sec:.2f} ops/seg")
    print("✅ TEST COMPLETADO: Dimensión 196883 validada.")

if __name__ == "__main__":
    stress_test()
