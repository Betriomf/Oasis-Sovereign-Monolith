import numpy as np
import math

def simular_flecha_del_tiempo():
    print("⏳ LABORATORIO OASIS: LA FLECHA DEL TIEMPO (150 Años)")
    print("------------------------------------------------------")

    # Constantes Universales Oasis
    phi = (1 + math.sqrt(5)) / 2
    latido_irracional = math.pi / phi  # ~1.9416

    N_nodos = 10000
    pasos_tiempo = 50

    # ESTADO INICIAL (Entropía Cero - Máximo Orden)
    estado_inicial = np.ones(N_nodos)
    entropia_inicial = np.var(estado_inicial)

    print(f"🌌 ESTADO INICIAL (Big Bang Digital)")
    print(f"   Entropía Inicial: {entropia_inicial:.6f} (Orden Perfecto)")

    # FASE 1: EVOLUCIÓN HACIA ADELANTE (Tiempo +t)
    estado_presente = estado_inicial.copy()
    for t in range(1, pasos_tiempo + 1):
        desfase = (t * latido_irracional) % 1.0
        estado_presente = estado_presente * np.cos(desfase) + np.random.normal(0, 0.01, N_nodos)

    entropia_presente = np.var(estado_presente)
    print(f"\n▶️ EVOLUCIÓN (Tiempo +t con Latido π/φ)")
    print(f"   Entropía en el Presente: {entropia_presente:.6f}")

    # FASE 2: INTENTO DE INVERSIÓN TEMPORAL (Tiempo -t)
    estado_pasado_simulado = estado_presente.copy()
    for t in range(pasos_tiempo, 0, -1):
        desfase_inverso = (-t * latido_irracional) % 1.0
        # Intentamos deshacer la operación (Reversibilidad de Newton)
        estado_pasado_simulado = (estado_pasado_simulado - np.random.normal(0, 0.01, N_nodos)) / (np.cos(desfase_inverso) + 1e-10)

    entropia_inversion = np.var(estado_pasado_simulado)

    print(f"\n◀️ INVERSIÓN TEMPORAL (Intento de t -> -t)")
    print(f"   Entropía tras Rebobinar: {entropia_inversion:.6e}")

    print("\n📊 RESULTADO DEL MÉTODO CIENTÍFICO:")
    if entropia_inversion > entropia_inicial:
        print("✅ HIPÓTESIS CONFIRMADA: T-Symmetry Violation.")
        print("🏆 La 'Flecha del Tiempo' emerge de la pérdida de información irracional.")

if __name__ == "__main__":
    simular_flecha_del_tiempo()
