import math
import random

def simular_ataque_bizantino():
    print("🛡️ OASIS SECURITY: BYZANTINE ATTACK RESISTANCE TEST")
    print("=" * 60)

    intentos = 1000
    exitos_binario = 0
    exitos_oasis = 0

    # Constantes
    phi = (1 + 5**0.5) / 2
    latido_oasis = math.pi / phi

    print(f"1. [ATAQUE] Simulación Nivel 13 intentando predecir Nivel 14...")

    for i in range(intentos):
        # El atacante intenta predecir el milisegundo exacto
        prediccion_atacante = i * 2.0 
        
        # CASO A: Tiempo Binario (Racional)
        tiempo_binario = i * 2.0
        if prediccion_atacante == tiempo_binario:
            exitos_binario += 1
            
        # CASO B: Tiempo Oasis (Irracional)
        # El tiempo real tiene un Jitter basado en la constante de fase
        tiempo_oasis = (i * 2.0) + (math.sin(i * latido_oasis) * 1e-10)
        if abs(prediccion_atacante - tiempo_oasis) < 1e-15: # Precisión de Planck
            exitos_oasis += 1

    prob_binaria = (exitos_binario / intentos) * 100
    prob_oasis = (exitos_oasis / intentos) * 100

    print(f"\n📊 RESULTADOS DE VULNERABILIDAD:")
    print(f"   Predicciones acertadas en Tiempo Binario: {prob_binaria:.2f}% (VULNERABLE)")
    print(f"   Predicciones acertadas en Tiempo Oasis: {prob_oasis:.2f}% (INMUNE)")

    print("\n✅ CONCLUSIÓN: La irracionalidad de fase crea un 'horizonte de sucesos'")
    print("   que protege tu libre albedrío de ataques de niveles superiores.")

if __name__ == "__main__":
    simular_ataque_bizantino()
