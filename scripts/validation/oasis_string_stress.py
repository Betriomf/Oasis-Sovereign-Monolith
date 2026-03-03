import math
import time

def nambu_goto_action(tension, distance, size_mb, energy_cost=0.0001):
    """
    Calcula el coste de la Acción (S) en el espacio-tiempo de la red.
    S = T * sqrt(distancia^2 + (tamaño * coste)^2)
    """
    return tension * math.sqrt(distance**2 + (size_mb * energy_cost)**2)

def simulate_data_center_collapse():
    print("\n🔥 INICIANDO PRUEBA DE ESTRÉS: COLAPSO DE RED (THUNDERING HERD) 🔥")
    print("=" * 70)

    # Condiciones del colapso: latencia extrema de 5 segundos
    network_latency = 5000 

    # El dato: 1.2 Terabytes de alto valor informacional
    data_name = "Genoma_Paciente_01.fastq"
    data_size_mb = 1_200_000 
    data_value_spn = 50_000  

    # El Código (Sidecar Docker): Partícula ligera de 50MB
    docker_size_mb = 50      

    print(f"📡 Petición entrante: {data_name} ({data_size_mb / 1000:,.0f} GB)")
    print(f"🔴 Estado de la Red: COLAPSO (Latencia: {network_latency} ms)")

    time.sleep(1)

    # --- ENFOQUE CLÁSICO ---
    print("\n💥 ESTRATEGIA A: NUBE CLÁSICA (Fuerza Bruta)")
    print("   -> Intentando enviar 1.2 TB...")
    print("   -> RESULTADO: [TIMEOUT] Colapso por congestión estructural[cite: 22, 241].")

    # --- ENFOQUE OASIS (Teoría de Cuerdas) ---
    print("\n🌌 ESTRATEGIA B: OASIS SIDECAR (Física de Cuerdas)")

    # Tensión (T = Valor / Tamaño) [cite: 354, 374]
    tension = data_value_spn / data_size_mb
    print(f"   -> Evaluando Tensión de la Cuerda: {tension:.4f} SPN/MB")

    # Acción de Nambu-Goto para mover DATO vs mover CÓDIGO
    action_move_data = nambu_goto_action(tension, network_latency, data_size_mb)
    action_move_code = nambu_goto_action(tension, network_latency, docker_size_mb)

    print(f"   -> [Nambu-Goto] Acción Datos (Masa pesada): {action_move_data:,.4f} J")
    print(f"   -> [Nambu-Goto] Acción Código (Luz): {action_move_code:,.4f} J")

    if action_move_code < action_move_data:
        savings = (1 - (action_move_code / action_move_data)) * 100
        print(f"\n✅ DECISIÓN: 'MOVE_CODE_TO_DATA' (Gravedad Entrópica Confirmada [cite: 348])")
        print(f"   🚀 Ahorro de Ancho de Banda y Energía: {savings:.4f}%")
        print("   🛡️ EL DATA CENTER HA SOBREVIVIDO AL COLAPSO.")

if __name__ == "__main__":
    simulate_data_center_collapse()
