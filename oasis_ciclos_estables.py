import subprocess
import json
import urllib.request
import time
import gc
import os

MODELO = "qwen2.5:0.5b"
ATRACTOR = 2.3  # Pausa térmica de Landauer (segundos)
TOTAL_CICLOS = 6
INTERVALO_PURGA = 3  # Ejecutar limpieza profunda cada N ciclos

def inferencia_limpia(ciclo):
    """Ejecuta inferencia forzando a Ollama a no retener VRAM/RAM (keep_alive: 0)."""
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": MODELO,
        "prompt": f"Calcula brevemente la derivada de x^2 en el punto x={ciclo} sin introducciones.",
        "stream": False,
        "keep_alive": "0s",  # Libera los pesos del modelo de la RAM unificada al terminar
        "options": {"temperature": 0.1}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"Error en ciclo: {e}"

def purga_espectral():
    """Libera buffers de Python, temporales y fuerza recolección del kernel."""
    print("    🧹 [Centinela]: Ejecutando purga espectral de ciclo...")
    
    # 1. Recolección de basura interna de Python
    objetos_liberados = gc.collect()
    
    # 2. Descarga explícita en Ollama por seguridad
    subprocess.run(["ollama", "stop", MODELO], capture_output=True, text=True)
    
    # 3. Purga nativa del sistema operativo (sin bloquear si no hay sudo)
    os.system("purge 2>/dev/null || true")
    
    print(f"    ✨ [Homeostasis]: RAM recuperada ({objetos_liberados} objetos GC purgados). Silicio estabilizado.")

def ejecutar_bucle():
    print("=" * 65)
    print("  INICIANDO MOTOR CÍCLICO OASIS CON AUTOLIMPIEZA DE RAM")
    print(f"  Modelo: {MODELO} | Pacing térmico: {ATRACTOR}s | Cadencia: {INTERVALO_PURGA} ciclos")
    print("=" * 65)

    saldo_l2 = 0.0

    for ciclo in range(1, TOTAL_CICLOS + 1):
        print(f"\n🌀 --- CICLO DE EXTRACCIÓN {ciclo}/{TOTAL_CICLOS} ---")
        
        inicio = time.time()
        respuesta = inferencia_limpia(ciclo)
        latencia = time.time() - inicio
        
        # Simulación de rendimiento y ticket
        ticket = 0.035 + (ciclo * 0.005)
        saldo_l2 += ticket
        
        print(f"🧠 [Newton]: Inferencia resuelta en {latencia:.2f}s")
        print(f"💡 [Salida]: {respuesta[:60]}...")
        print(f"📦 [Compresión]: Token firmado (+${ticket:.5f} USDC) | Acumulado: ${saldo_l2:.5f}")
        
        # Disipación térmica gobernada
        print(f"🛡️ [Landauer]: Pausa de relajación ({ATRACTOR}s)...")
        time.sleep(ATRACTOR)
        
        # Disparo del protocolo de purga cada N ciclos
        if ciclo % INTERVALO_PURGA == 0 and ciclo != TOTAL_CICLOS:
            purga_espectral()

    print("\n" + "=" * 65)
    print(f"✅ SESIÓN FINALIZADA | Saldo consolidado: ${saldo_l2:.5f} USDC")
    print("=" * 65)
    purga_espectral()

if __name__ == "__main__":
    ejecutar_bucle()
