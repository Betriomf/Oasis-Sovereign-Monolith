import time
import math
import subprocess

# Parámetros de la Línea Crítica de Riemann y Fibonacci
PHI = (1 + math.sqrt(5)) / 2
KAPPA_M = -0.6587

def verify_phase(input_signal):
    """
    Verificación en tiempo P (Polinómico/Frío).
    Solo si la señal resuena con Phi, se permite el paso.
    """
    check = (input_signal * PHI) % 1
    # Umbral de tolerancia Oasis (0.158 rad de jitter)
    return abs(check - 0.5) < 0.158

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
    print("🛰️ OASIS THERMAL SHIELD ACTIVE - DIMENSIÓN 196883")
    # Prueba 1: Señal en fase (Sintonizada)
    secure_gateway(0.309) # Valor armónico
    # Prueba 2: Señal de Mythos (Ruido)
    secure_gateway(0.999) # Intento de intrusión
