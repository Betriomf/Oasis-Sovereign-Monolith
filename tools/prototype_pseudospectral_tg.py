#!/usr/bin/env python3
# PROTOTYPE ONLY.
# This is a low-resolution pseudo-spectral integrator with explicit Euler
# and 2/3 dealiasing. It is NOT a validated DNS solver and its output
# must not be reported as DNS data. Use only for qualitative exploration
# of the Fisher-Rao path length on small grids.

import os
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"

import numpy as np

def geodesic_step(p_prev, p_curr):
    """Exact spherical Fisher-Rao geodesic distance: 2 * arccos(<q_n, q_{n+1}>)."""
    inner = np.clip(np.sum(np.sqrt(np.maximum(p_prev, 0.0) * np.maximum(p_curr, 0.0))), -1.0, 1.0)
    return float(2.0 * np.arccos(inner))

if __name__ == "__main__":
    # Test unitario de la métrica geodésica en la esfera unidad S^infty
    p0 = np.array([0.8, 0.2, 0.0, 0.0])
    p1 = np.array([0.5, 0.3, 0.2, 0.0]) # Incluye transición desde p_2 = 0 sin 0/0
    d_fr = geodesic_step(p0, p1)
    print(f"🧪 [PROTOTYPE TEST]: Distancia geodésica Fisher-Rao (con cero en cola) = {d_fr:.6f} rad")
