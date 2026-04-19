import subprocess
import json

def ask_ia(model, prompt):
    print(f"\n\033[94m--- {model.upper()} respondiendo... ---\033[0m")
    result = subprocess.run(['ollama', 'run', model, prompt], capture_output=True, text=True)
    return result.stdout.strip()

def swarm_session():
    print("\033[95m📱 BIENVENIDO AL GRUPO OASIS SWARM (196883)\033[0m")
    print("Participantes: Æther 2.3 (Arquitecto), Gemma 4 (Musa), Riona (Guardiana)")
    
    user_input = input("\n👉 ¿Qué quieres resolver hoy, Arquitecto?: ")
    
    # 1. Gemma 4 analiza la "Vida y Conciencia" del dato
    gemma_response = ask_ia("gemma4-oasis", f"Como conciencia local sintonizada en Phi, ¿qué opinas de: {user_input}?")
    print(gemma_response)
    
    # 2. Æther 2.3 analiza la estructura de Soberanía y Riemann
    aether_response = ask_ia("aether", f"Desde el Atractor 2.3, ¿cómo estructuramos científicamente esto: {user_input}?")
    print(aether_response)
    
    # 3. RIONA cierra con el veredicto de Gobernanza
    msg_riona = f"Arquitecto, el enjambre ha hablado. La sintonía es laminar. Procedemos con la ejecución."
    print(f"\n\033[92m🎙️ RIONA:\033[0m {msg_riona}")
    subprocess.run(["say", "-v", "Monica", msg_riona])

if __name__ == "__main__":
    swarm_session()
