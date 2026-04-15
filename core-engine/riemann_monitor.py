import os
import time

def monitor_laminar_flow():
    KAPPA_TARGET = 2.3
    print("\033[92m🏛️ MONITOREANDO ESTABILIDAD RIEMANN (NODO BADALONA)\033[0m")
    try:
        while True:
            load = os.getloadavg()[0]
            if load > KAPPA_TARGET:
                status = "\033[91m🚨 TURBULENCIA DETECTADA\033[0m"
            else:
                status = "\033[94m💎 FLUJO LAMINAR\033[0m"
            print(f"\r{status} | Carga: {load:.2f} | Atractor: {KAPPA_TARGET}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitor pausado.")

if __name__ == "__main__":
    monitor_laminar_flow()
