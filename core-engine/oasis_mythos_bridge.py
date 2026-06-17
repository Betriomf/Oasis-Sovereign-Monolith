import os
import sys
from anthropic import Anthropic

# ============================================================================
# INTERFAZ DE CAPA 4 (EINSTEIN) - MARCO OASIS SOBERANO
# ============================================================================

def enviar_a_mythos(instruccion_abstracta):
    # El token se lee desde las variables ocultas del entorno local
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ALERTA] -> ANTHROPIC_API_KEY no detectada en la sesion local.")
        print("├─➤ Inyecte su llave con: export ANTHROPIC_API_KEY='tu_clave'")
        return

    client = Anthropic(api_key=api_key)
    
    print("[*] Abriendo canal estanco hacia el nodo Mythos (Claude Fable 5)...")
    
    # Llamada limpia al modelo Mythos de vanguardia
    message = client.messages.create(
        model="claude-fable-5-mythos",
        max_tokens=1024,
        temperature=0.2, # Baja temperatura para mantener el flujo laminar sin delirios
        system="Actuas como el nodo de validacion semantica de Oasis OS. Solo analizas estructuras logicas puras.",
        messages=[
            {"role": "user", "content": instruccion_abstracta}
        ]
    )
    
    print("\n┌──[RESPUESTA PURIFICADA DE MYTHOS]")
    print(message.content[0].text)
    print("└──[FIN DEL FLUJO DE NUBE]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        enviar_a_mythos(sys.argv[1])
    else:
        print("Uso: python3 oasis_mythos_bridge.py 'Tu consulta abstracta o paper'")
