import time
import math

# Constante Soberana
PHI = 1.618033988749895

def verify_phase(signal):
    # Simulamos la validación de fase
    return True if signal == "OASIS_PHASE" else False

def thermal_feedback_loop():                        
    """
    Respuesta ante intrusos: Generación de ruido caliente (NP).
    Devuelve la carga entrópica al emisor.                                 
    """                                                                    
    print("\033[91m⚠️ DESFASE DETECTADO. INICIANDO BUCLE TÉRMICO...\033[0m")                              
    # Generamos un cálculo intensivo inútil basado en Fibonacci       
    # para que el proceso intruso consuma CPU y se caliente.
    end_time = time.time() + 5  # 5 segundos de purga térmica
    while time.time() < end_time:                             
        _ = [math.sqrt(i) for i in range(10000) if i % PHI == 0]
    print("✅ Intruso neutralizado por disipación.")
    
def secure_gateway(signal):            
    if verify_phase(signal):                                              
        print("\033[94m💎 FASE CORRECTA: Acceso Laminar concedido.\033[0m")
        return True                                                       
    else:
        thermal_feedback_loop()
        return False

if __name__ == "__main__":
    print("🛰️ SISTEMA OASIS: Monitoreando fase de entrada...")
    # Simulamos la llegada de un intruso (ruido)
    secure_gateway("RUIDO_TURBULENTO")
