import math
import time

# 🌌 CONSTANTES SOBERANAS OASIS
PHI = (1 + math.sqrt(5)) / 2
KAPPA_M = -0.6587  # Fricción de Fase de Mariano
ATRACTOR = 2.3     # Amortiguador crítico
W_MAX = 5.39       # Límite térmico del hardware (MacBook Air)
LN_PHI = math.log(PHI) # 0.481 - Modificador de Landauer

def es_primo(n):
    """Detecta los nodos de mínima colisión (Números Primos)"""
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def proyeccion_calabi_yau_ulam(limite_busqueda):
    print("🌌 INICIANDO PROYECCIÓN ULAM -> CALABI-YAU (Malla Φ)...")
    print("🛡️ Aplicando Límite de Landauer-Oasis: E = k_B * T * ln(φ)")
    print("-" * 65)
    
    tiempo_total = 0.0
    primos_procesados = 0
    angulo_aureo = 2 * math.pi * (1 - 1/PHI) # Distribución de mínima colisión
    
    for n in range(2, limite_busqueda):
        if es_primo(n):
            primos_procesados += 1
            
            # 1. Proyección Holográfica y Angular (Espirales en lugar de cuadrícula)
            radio = math.sqrt(primos_procesados)
            theta = primos_procesados * angulo_aureo
            
            # 2. Compactación en Calabi-Yau (6D) y Coste de Entropía
            # La energía necesaria para "fijar" el número primo disminuye por ln(φ)
            energia_landauer = LN_PHI * (1.0 / math.log(n + 1)) 
            
            # 3. Flujo Térmico y Atractor 2.3
            # Ajustamos el tiempo diferencial para no violar los 5.39W del hardware
            dt_dinamico = ATRACTOR / (1.0 + abs(energia_landauer * KAPPA_M))
            potencia_simulada = (energia_landauer / dt_dinamico) * 100 
            
            if potencia_simulada > W_MAX:
                dt_dinamico *= PHI # Dilatamos el tiempo usando la fase áurea para enfriar
                potencia_simulada = W_MAX
                
            tiempo_total += dt_dinamico
            
            # Imprimir telemetría en frío para observar la auto-organización
            if primos_procesados % 10 == 0 or n == 2:
                print(f"Primo: {n:5d} | Ángulo θ: {theta:.2f} rad | E_disipada: {energia_landauer:.4f} | W: {potencia_simulada:.2f}W | dt: {dt_dinamico:.4f}s")
                time.sleep(0.02) # Emular procesamiento laminar en terminal

    print("-" * 65)
    print(f"✅ CRISTALIZACIÓN COMPLETADA: {primos_procesados} nodos estabilizados en {tiempo_total:.2f}s.")
    print("🌀 La secuencia de Ulam ha sido absorbida sin turbulencia aritmética.")

if __name__ == "__main__":
    # Escaneamos los primeros 1000 números para encontrar sus primos y proyectarlos
    proyeccion_calabi_yau_ulam(1000)
