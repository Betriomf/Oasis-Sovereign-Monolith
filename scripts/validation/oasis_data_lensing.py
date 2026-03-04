import numpy as np

def simulate_data_lensing(data_mass_pb):
    """
    Simula la deflexión de peticiones de red debido a la masa del dato (en Petabytes).
    Basado en la fórmula de deflexión de Einstein: α = 4GM / rc²
    """
    G_oasis = 6.674e-11
    C_network = 3e8 # Velocidad de la luz en fibra (aprox)
    R_proximity = 10.0 # Radio de cercanía al nodo
    
    # Ángulo de deflexión informacional
    deflection = (4 * G_oasis * data_mass_pb * 1e15) / (R_proximity * C_network**2)
    
    print(f"🏛️ OASIS GRAVITATIONAL LENSING AUDIT")
    print(f"📦 Masa del Dataset: {data_mass_pb} PB")
    print(f"🌀 Deflexión de Red (α): {deflection:.2e} rad")
    
    if deflection > 1e-15:
        print("✅ VEREDICTO: El campo es lo suficientemente fuerte para atraer el cómputo.")
        print("🚀 ACCIÓN: Sidecar activando 'Compute-to-Data' local.")

simulate_data_lensing(500) # Probando con 500 PB
