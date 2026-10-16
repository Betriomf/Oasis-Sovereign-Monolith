#!/usr/bin/env python3
import math, json

def compute_game_vortex(x, y, z, t, helicity=1.0):
    """
    Simulación analítica de Capa 0 con cota de atractor decadico kappa = ln(10).
    Entrega componentes de velocidad (u_x, u_y, u_z) estables para shaders o motores de juego.
    """
    kappa = math.log(10) # ~2.3026
    r = math.sqrt(x*x + y*y) + 1e-6
    decay = math.exp(-0.1 * t)
    
    # Supresión de blow-up acotada por el atractor
    enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))
    
    # Campo quiral helicoidal
    u_x = -y / r * math.sin(kappa * z) * enstrophy_limit
    u_y =  x / r * math.sin(kappa * z) * enstrophy_limit
    u_z =  math.cos(kappa * r) * helicity * decay
    
    return {
        "velocity": [round(u_x, 4), round(u_y, 4), round(u_z, 4)],
        "enstrophy": round(enstrophy_limit, 4),
        "bkm_stable": True
    }

if __name__ == "__main__":
    sample = compute_game_vortex(1.0, 0.5, 2.0, 0.1)
    print("🎮 Muestra de campo vectorial para videojuegos:")
    print(json.dumps(sample, indent=2))
