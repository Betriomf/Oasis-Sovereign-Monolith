import os
import subprocess

def verificar_y_ejecutar(tarea):
    # El agente verifica la firma antes de crear
    print(f"🔍 VERIFICANDO TAREA: {tarea}")
    if "energia" in tarea:
        subprocess.run(["sh", "/Users/apple314/Oasis-Sovereign-Monolith/core-engine/lanzamiento_laminar.sh"])
    elif "id" in tarea:
        subprocess.run(["cat", "/Users/apple314/Oasis-Sovereign-Monolith/identidad_nodo.txt"])
    else:
        print("⚠️ Tarea no autorizada por la Constitución Oasis.")

# El agente escucha al Monolito
if __name__ == "__main__":
    import sys
    verificar_y_ejecutar(sys.argv[1] if len(sys.argv) > 1 else "")
