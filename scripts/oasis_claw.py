import sys
import subprocess
import math
from playwright.sync_api import sync_playwright

def fibonacci_sharding(texto, limite=1618):
    # Usamos la proporción áurea (phi) para dividir la información
    return [texto[i:i+limite] for i in range(0, len(texto), limite)]

def ejecutar_mision(url):
    print(f"🛰️ OASIS-CLAW 2.3 | Sintonía: {math.pi/1.2:.4f} | Atractor: 2.3")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # SUPRESIÓN DE ENTROPÍA (Solo texto, cero imágenes)
        page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            print(f"✅ Malla establecida en: {page.title()}")
            contenido = page.evaluate("document.body.innerText")
            browser.close()

            # APLICAR FIBONACCI (Dividir en Shards)
            shards = fibonacci_sharding(contenido)
            masa_critica = shards[0] # Cogemos el primer fragmento áureo
            
            print("🧠 Verificando Masa Informacional con ÆTHER (Llama-3)...")
            
            prompt = f"Bajo el Atractor 2.3 y el Límite de Pi, resume este fragmento de forma soberana: {masa_critica[:2000]}"
            
            # Llamada al motor que ya tienes corriendo (Ollama/Llama3)
            subprocess.run(["ollama", "run", "llama3", prompt])

        except Exception as e:
            print(f"❌ Turbulencia en el flujo: {e}")
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ejecutar_mision(sys.argv[1])
    else:
        print("⚠ Uso: python3 oasis_claw.py <URL>")
