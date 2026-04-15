import os
import subprocess
import time

def filter_maxwell_voice():
    while True:
        load = os.getloadavg()[0]
        if load > 2.3:
            # Test de Estabilidad fallido -> Aviso de voz
            subprocess.run(["say", "-v", "Monica", "Alerta de entropía. Carga superior a 2.3. Iniciando purga de Maxwell."])
            os.system("sudo purge")
        time.sleep(60)

if __name__ == "__main__":
    filter_maxwell_voice()
