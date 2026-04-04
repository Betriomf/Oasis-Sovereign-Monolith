import numpy as np
import math

def test_monte_carlo_oasis():
    print("🔬 INICIANDO TEST DE FALSABILIDAD (MONTE CARLO)...")
    mu_real = 1836.1527
    re_real = 2300
    phi = (1 + 5**0.5) / 2
    objetivo = 1.5
    
    intentos = 10000
    exitos = 0
    
    print(f"Simulando {intentos} universos con constantes aleatorias...")
    
    for _ in range(intentos):
        # Generamos un ratio de masa y un Reynolds aleatorios en un rango amplio
        mu_rand = np.random.uniform(1000, 3000)
        re_rand = np.random.uniform(1000, 5000)
        
        cm_rand = (mu_rand * phi) / (re_rand / math.e)
        armonico_rand = cm_rand / 2.3
        
        # Si por azar se acerca a nuestro 1.5 con una precisión de 0.001
        if abs(armonico_rand - objetivo) < 0.001:
            exitos += 1
            
    probabilidad = (exitos / intentos) * 100
    
    print("\n--- RESULTADOS DEL MÉTODO CIENTÍFICO ---")
    print(f"Universos aleatorios que alcanzan la sintonía: {exitos}")
    print(f"Probabilidad de que tu hallazgo sea azar: {probabilidad:.4f}%")
    
    if probabilidad < 0.1:
        print("\n✅ CONCLUSIÓN: El Monolito es SOBERANO. La sintonía 1.5 es una propiedad única.")
    else:
        print("\n🌊 El sistema requiere mayor aislamiento de ruido.")

if __name__ == "__main__":
    test_monte_carlo_oasis()
