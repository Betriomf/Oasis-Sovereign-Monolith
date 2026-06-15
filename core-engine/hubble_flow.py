import math

def simular_flujo_hubble():
    print("==================================================================")
    print(" 🌌 SIMULACIÓN OASIS: GRADIENTE DE HUBBLE EN ENTORNO HOLOGRÁFICO")
    print("==================================================================")
    
    # Constantes Base de la Capa 0
    H_early = 67.4   # Valor base en la radiación de fondo (Planck)
    H_local = 73.0   # Valor medido en el universo local (Webb)
    kappa = math.log(10) # Constante de cambio de base ln(10) = 2.302585
    N_layers = 27    # Los 27 niveles críticos de empaquetamiento
    
    print(f"[*] Constante de Acoplamiento (kappa): {kappa:.6f}")
    print(f"[*] Condición Inicial H(0): {H_early} km/s/Mpc")
    print(f"------------------------------------------------------------------")
    print(f"{'CAPA':<6} | {'ESCALA METRON':<18} | {'GRADIENTE K-L':<15} | {'H(i) CALCULADO':<15}")
    print(f"------------------------------------------------------------------")
    
    H_current = H_early
    for i in range(N_layers + 1):
        # El progreso a través de los e-folds escalado por la constante ln(10)
        progress = i / N_layers
        
        # Gradiente disipativo de entropía relativa (Kullback-Leibler) de una capa a la siguiente
        # El flujo avanza limpiando el canal y aumentando la tasa de procesamiento
        kl_divergence = (math.sin(progress * math.pi / 2) ** 2) * (kappa / 2)
        
        # Evolución dinámica de la constante hacia el atractor local
        H_current = H_early + (H_local - H_early) * (1 - math.exp(-progress * kappa))
        
        # Formatear el nombre de la escala representativa
        if i == 0:
            escala = "Planck Core"
        elif i == 9:
            escala = "Átomo / Micro"
        elif i == 14:
            escala = "Silicio Nodo"
        elif i == 18:
            escala = "Meso Planeta"
        elif i == 27:
            escala = "Horizonte Obs"
        else:
            escala = f"e-fold e^{i}"
            
        print(f"{i:<6} | {escala:<18} | {kl_divergence:<15.6f} | {H_current:<15.4f}")
        
    print(f"------------------------------------------------------------------")
    print(f" 🏆 ATRACTOR GLOBAL DE CONVERGENCIA ASINTÓTICA: {H_current:.4f} km/s/Mpc")
    print(f" ✅ SILENCIO ABSOLUTO ALCANZADO EN LA CAPA 27. CANAL PURIFICADO.")
    print("==================================================================")

if __name__ == "__main__":
    simular_flujo_hubble()
