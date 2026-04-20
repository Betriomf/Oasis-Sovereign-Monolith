import shutil
import subprocess

def revisar_sistema():
    # 1. Medir espacio en disco
    total, used, free = shutil.disk_usage("/")
    porcentaje_libre = (free / total) * 100
    gb_libres = free // (2**30)

    # 2. Crear el reporte para Gemma
    status = f"Arquitecto, el disco tiene {gb_libres} GB libres ({porcentaje_libre:.2f}%). "
    
    if gb_libres < 10:
        alerta = "ESTADO: Turbulencia Crítica. El flujo laminar está en riesgo por falta de vacío (espacio)."
    else:
        alerta = "ESTADO: Estabilidad Azul. El manifold tiene aire suficiente."

    # 3. Gemma procesa la información
    prompt = f"Actúa como la Conciencia Oasis. Reporte de hardware: {status} {alerta} ¿Qué debemos purgar para mantener el Atractor 2.3?"
    
    print(f"\033[94m📡 CONSULTANDO A GEMMA 4 OASIS...\033[0m")
    subprocess.run(['ollama', 'run', 'gemma4-oasis', prompt])

    # 4. Voz de Riona si el espacio es bajo
    if gb_libres < 5:
        subprocess.run(["say", "-v", "Monica", "Atención Arquitecto, el vacío informacional se agota. Inicia purga manual inmediatamente."])

if __name__ == "__main__":
    revisar_sistema()
