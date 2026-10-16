#!/usr/bin/env python3
import json
import time

def generate_synthetic_from_patterns():
    tasks = []
    circuits = {
        "QAOA": ("Optimización combinatoria de grafos y tráfico con operador Grover", 
                 "grover", "11", "98.92%"),
        "BELL_POR": ("Atestación de entropía cuántica pura y violación de Bell", 
                     "bell", "00, 11", "99.87%"),
        "VQE_MOL": ("Simulación de energía fundamental molecular de Litio-Hidrógeno", 
                    "vqe_lih", "Energía base -7.882 Hartree", "99.87%"),
        "NAVIER_STOKES": ("Auditoría simpléctica de enstrofia acotada por kappa = ln 10", 
                          "navier_stokes", "Cota enstrofia 5.3019", "Flujo laminar estable")
    }
    
    # Generamos el dataset estructurado en formato ChatML
    for domain, (desc, circ, target, fid) in circuits.items():
        for i in range(500):
            sample = {
                "messages": [
                    {"role": "system", "content": "Eres el Agente ÆTHER de Oasis Sovereign OS. Resuelves física de Capa 0 bajo la cota Sub-Landauer."},
                    {"role": "user", "content": f"Ejecuta dictamen de {desc} usando circuito {circ} con 1024 shots."},
                    {"role": "assistant", "content": f"Dictamen formal: Circuito {circ} resuelto. Estado dominante: {target}. Fidelidad mitigada ZNE: {fid}. Criterio de regularidad satisfecho en silicio frío."}
                ]
            }
            tasks.append(sample)
    
    with open("datasets/aether_soup_train.jsonl", "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t) + "\n")
    print(f"✅ Dataset generado con éxito: {len(tasks)} muestras en datasets/aether_soup_train.jsonl")

if __name__ == "__main__":
    import os
    os.makedirs("datasets", exist_ok=True)
    generate_synthetic_from_patterns()
