import numpy as np
import time

def simulate_phi_scheduling(n_nodes=1000):
    phi = (1 + 5**0.5) / 2
    # Sincronización irracional vs Racional
    irrational_times = [(i * phi) % 1.0 for i in range(n_nodes)]
    rational_times = [(i * 0.5) % 1.0 for i in range(n_nodes)]
    
    def get_collisions(times, delta=0.001):
        times.sort()
        collisions = sum(1 for i in range(len(times)-1) if times[i+1] - times[i] < delta)
        return collisions

    print(f"Colisiones Racionales: {get_collisions(rational_times)}")
    print(f"Colisiones OASIS (Phi): {get_collisions(irrational_times)}")

simulate_phi_scheduling()
