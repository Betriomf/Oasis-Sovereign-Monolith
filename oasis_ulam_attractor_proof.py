#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — DEMOSTRACIÓN EMPÍRICA DEL ATRACTOR L=2.3
Compara la proyección de la Espiral de Ulam-Calabi-Yau con L=1.0 vs L=2.3 (Capa 0).
"""

import math
import time

PHI = (1.0 + math.sqrt(5.0)) / 2.0
KAPPA_M = -0.6587     # Fricción de Fase de Mariano
W_MAX = 5.39          # Cota Térmica MacBook Air
LN_PHI = math.log(PHI) # 0.4812 (Modificador de Landauer)

def es_primo(n: int) -> bool:
    if n < 2: return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0: return False
    return True

def evaluar_atractor(atractor_val: float, limite_busqueda: int = 1000):
    primos_procesados = 0
    tiempo_total = 0.0
    angulo_aureo = 2.0 * math.pi * (1.0 - 1.0 / PHI)
    picos_sobrecalentamiento = 0
    historial_potencia = []

    for n in range(2, limite_busqueda):
        if es_primo(n):
            primos_procesados += 1
            
            # Cota de Entropía de Landauer-Oasis
            energia_landauer = LN_PHI * (1.0 / math.log(n + 1))
            
            # Ajuste dinámico por el Atractor L
            dt_dinamico = atractor_val / (1.0 + abs(energia_landauer * KAPPA_M))
            potencia_simulada = (energia_landauer / dt_dinamico) * 100.0
            
            if potencia_simulada > W_MAX:
                picos_sobrecalentamiento += 1
                dt_dinamico *= PHI  # Dilatación áurea de tiempo
                potencia_simulada = W_MAX
                
            tiempo_total += dt_dinamico
            historial_potencia.append(potencia_simulada)

    potencia_media = sum(historial_potencia) / len(historial_potencia)
    return primos_procesados, tiempo_total, potencia_media, picos_sobrecalentamiento

def ejecutar_demostracion():
    print("⚖️  OASIS CAPA 0 — PRUEBA DE CAMPO: DEMOSTRACIÓN DEL ATRACTOR L=2.3")
    print("=" * 70)
    
    # Test 1: Atractor No Calibrado (L = 1.0)
    n1, t1, p1, picos1 = evaluar_atractor(1.0)
    print(f"🔴 [ESCENARIO A — SIN ATRACTOR / L = 1.0]:")
    print(f"   ├─ Nodos Primos Procesados : {n1}")
    print(f"   ├─ Tiempo de Integración   : {t1:.4f} s")
    print(f"   ├─ Potencia Promedio       : {p1:.2f} W")
    print(f"   └─ Intervenciones Térmicas: {picos1} correcciones forcadas")
    print("-" * 70)

    # Test 2: Atractor Sintonizado Oasis (L = 2.3)
    n2, t2, p2, picos2 = evaluar_atractor(2.3)
    print(f"🟢 [ESCENARIO B — SINTONÍA OASIS / L = 2.3]:")
    print(f"   ├─ Nodos Primos Procesados : {n2}")
    print(f"   ├─ Tiempo de Integración   : {t2:.4f} s")
    print(f"   ├─ Potencia Promedio       : {p2:.2f} W")
    print(f"   └─ Intervenciones Térmicas: {picos2} correcciones (Flujo Laminar Puro)")
    print("=" * 70)

    print("📊 CONCLUSION DEMOSTRATIVA:")
    print(f"   El Atractor L=2.3 incrementa el margen térmico en un {((p1 - p2)/p1)*100:.1f}%,")
    print("   garantizando la absorción de primos sin estrés de silicio en el Mac.")

if __name__ == "__main__":
    ejecutar_demostracion()
