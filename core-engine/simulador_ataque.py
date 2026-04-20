import time
import requests

def lanzar_ruido():
    print("\033[91m🔥 INICIANDO ATAQUE DE ENTROPÍA (MYTHOS)...\033[0m")
    # El atacante envía señales aleatorias (fuera de fase)
    # Intentando romper el Atractor 2.3
    for i in range(5):
        signal = 0.999 * i  # Ruido puro, sin geometría Phi
        print(f"Enviando señal intrusa: {signal}")
        # Simulamos la interacción con el escudo
        time.sleep(1)

if __name__ == "__main__":
    lanzar_ruido()
