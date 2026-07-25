#!/usr/bin/env python3
import time
import urllib.request
import json

def test_inference(prompt):
    url = "http://127.0.0.1:11434/api/generate"
    data = json.dumps({"model": "qwen2.5:0.5b", "prompt": prompt, "stream": False}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    start = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            elapsed = time.time() - start
            eval_count = res.get('eval_count', 1)
            tps = eval_count / elapsed
            return elapsed, tps
    except Exception as e:
        print(f"⚠️ Error al conectar con Ollama: {e}")
        return None, None

if __name__ == "__main__":
    print("🌌 [OASIS BENCHMARK - TEST DE 1 CLIC]")
    print("---------------------------------------")
    prompt = "Responde brevemente: ¿Qué es la conservación de la energía en 1 frase?"
    t, tps = test_inference(prompt)
    if t:
        print(f"⚡ Tiempo de Respuesta: {t:.2f} segundos")
        print(f"🚀 Velocidad: {tps:.2f} tokens/segundo")
        print("✅ Régimen de prueba finalizado con éxito.")
