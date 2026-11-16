#!/usr/bin/env python3
import sys, json, time, urllib.request

model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5:1.5b"
prompt = sys.argv[2] if len(sys.argv) > 2 else "Explica el invariante causal de Minkowski en 3 líneas."
est_tokens = 120  # Estimación base para calcular ETA

payload = json.dumps({
    "model": model,
    "prompt": prompt,
    "stream": True,
    "keep_alive": -1,  # Mantiene el modelo anclado en RAM (0s de carga en siguientes consultas)
    "options": {"num_thread": 2, "temperature": 0.618}
}).encode("utf-8")

req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})

t_start = time.time()
t_first = None
tokens = 0

print(f"❄️  Cargando/Anclando [{model}] en RAM (2 hilos)...")
with urllib.request.urlopen(req, timeout=120) as resp:
    for line in resp:
        if not line:
            continue
        chunk = json.loads(line.decode("utf-8"))
        if t_first is None:
            t_first = time.time()
            print(f"⚡ Primer token en {t_first - t_start:.2f}s. Generando flujo:\n")
        
        piece = chunk.get("response", "")
        sys.stdout.write(piece)
        sys.stdout.flush()
        tokens += 1

        # Actualizar ETA en la barra de título de la terminal
        elapsed_gen = max(time.time() - t_first, 0.01)
        tps = tokens / elapsed_gen
        rem = max(est_tokens - tokens, 0)
        eta = rem / tps if tps > 0 else 0
        sys.stdout.write(f"\033]0;[{model}] {tokens} toks | {tps:.1f} tok/s | ETA: {eta:.1f}s\007")

total_t = time.time() - t_start
print(f"\n\n✅ Completado: {tokens} tokens en {total_t:.2f}s ({tokens/max(total_t,0.01):.2f} tok/s) | Modelo fijado en RAM.")
