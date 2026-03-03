import numpy as np

def verify_stability(kappa=2.3):
    # Basado en la ley Teff = Tbase * e^(-S/kappa) [cite: 210, 260]
    # Y el exponente de Lyapunov lambda = -1/kappa [cite: 219]
    lyapunov_exponent = -1 / kappa
    is_stable = lyapunov_exponent < 0 [cite: 219]
    print(f"--- OASIS STABILITY CHECK (kappa={kappa}) ---")
    print(f"Lyapunov Exponent (λ): {lyapunov_exponent:.4f}")
    print(f"Estado de Convergencia: {'ESTABLE (Mínima Fricción)' if is_stable else 'INESTABLE'}")
    return is_stable

verify_stability()
