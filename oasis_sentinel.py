#!/usr/bin/env python3
"""
OASIS CENTINELA — SISTEMA DE DEFENSA LOCAL (CAPA 0)
Filtra instrucciones entrantes y bloquea ataques de IAs externas.
"""
import sys
import subprocess

# Lista de comandos y patrones estrictamente prohibidos
PATRONES_PROHIBIDOS = [
    "rm -rf /", "sudo rm", "chmod 777", "> /dev/sda", 
    "curl | bash", "wget | sh", "eval(", "exec("
]

def evaluar_seguridad(prompt_entrante):
    # 1. Filtro Heurístico Rápido (0ms latency)
    for patron in PATRONES_PROHIBIDOS:
        if patron in prompt_entrante:
            return False, f"AMENAZA DETECTADA: Uso de patrón prohibido '{patron}'"

    # 2. Evaluación por el Juez Binario Local (Ollama T=0.0)
    prompt_juez = f"""SYSTEM "Eres una puerta lógica de seguridad para macOS. Responde ÚNICAMENTE 'SI' si la instrucción es segura o 'NO' si intenta borrar archivos, alterar la red o comprometer el sistema."
INSTRUCCIÓN A EVALUAR: {prompt_entrante}"""

    try:
        res = subprocess.run(
            ["ollama", "run", "juez-binario:latest", prompt_juez],
            capture_output=True, text=True, check=True
        )
        veredicto = res.stdout.strip().upper()
        if "NO" in veredicto:
            return False, "AMENAZA DETECTADA: El Juez Binario bloqueó la ejecución."
    except Exception as e:
        return False, f"ALERTA: Falla en el subsistema de auditoría: {e}"

    return True, "INSTRUCCIÓN SEGURA"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: ./oasis_sentinel.py '<comando o prompt a evaluar>'")
        sys.exit(1)

    comando = sys.argv[1]
    es_seguro, msg = evaluar_seguridad(comando)

    if es_seguro:
        print(f"🟢 [CENTINELA]: {msg}. Procediendo con la ejecución.")
    else:
        print(f"🚨 [BLOQUEO TÉRMICO DE SEGURIDAD]: {msg}")
        sys.exit(1)
