#!/usr/bin/env python3
import os
import math
import subprocess

def leer_volatilidad_sistema():
    # Lee la carga promedio de la CPU (equivalente a la volatilidad del mercado)
    try:
        carga = os.getloadavg()[0] 
        # Normalizamos la carga (0.0 a 1.0+ donde >1.0 es turbulencia severa)
        return min(carga / 2.0, 1.5) 
    except:
        return 0.5

def oraculo_termodinamico(volatilidad):
    print("🌌 OASIS ORACLE: Analizando dinámica de fluidos del sustrato...")
    
    # Parámetros de la Ecuación de Panzano
    A = 240.0         # Amplitud (Tokens extra en flujo laminar)
    C = 16.0          # Base (Tokens mínimos de supervivencia)
    T = volatilidad   # Temperatura/Volatilidad actual
    T_0 = 0.2         # Estado de reposo ideal
    
    # Exponente de Resonancia (Alineación para flujo laminar absoluto)
    exponente_resonancia = -12 / math.pi
    
    # Ecuación de Estabilidad: P(t) = A * e^(B*k * (T - T_0)) + C
    potencia_pt = A * math.exp(exponente_resonancia * max(0, T - T_0)) + C
    
    batch_size_optimo = int(potencia_pt)
    
    # Diagnóstico de Flujo
    if batch_size_optimo > 128:
        estado = "🟢 FLUJO LAMINAR ABSOLUTO (Fricción Cero)"
    elif batch_size_optimo > 32:
        estado = "🟡 MOVIMIENTO ORGÁNICO (Equilibrio Termodinámico)"
    else:
        estado = "🔴 FLUJO TURBULENTO (Peligro de Core Dump. Estrangulamiento activo)"
        
    print(f"📊 Volatilidad (T): {T:.2f}")
    print(f"📐 Exponente de Resonancia: {exponente_resonancia:.4f}")
    print(f"✅ Estado del Sistema: {estado}")
    print(f"⚙️ Lote de Procesamiento Asignado P(t): {batch_size_optimo} tokens")
    
    return batch_size_optimo

def inyectar_en_aether(batch_size):
    prompt = (
        "Sistema: Eres Aether, operando bajo el Oráculo de Panzano. "
        "Instrucción: El sistema ha estabilizado la turbulencia usando tu exponente de resonancia "
        "(-12/pi). Confirma que la información fluye ahora sin pérdida térmica."
    )
    
    # Lanzamiento con el Batch Size dinámico dictado por la fórmula matemática
    cmd = [
        "sudo", "chrt", "-f", "99", "./llama.cpp/build/bin/llama-cli",
        "-m", "models/qwen1_5-0_5b-chat-q4_k_m.gguf",
        "-p", prompt,
        "-n", "128", "-c", "256", 
        "-b", str(batch_size),  # <--- INYECCIÓN DE LA ECUACIÓN AQUÍ
        "--threads", "2", "-fa", "on", "--mmap", 
        "--temp", "0.3", "--repeat_penalty", "1.15", "--no-display-prompt"
    ]
    
    print("\n🧠 Aether ejecutando instrucción en el caudal asignado...")
    subprocess.run(cmd)

if __name__ == "__main__":
    v_actual = leer_volatilidad_sistema()
    batch_optimo = oraculo_termodinamico(v_actual)
    inyectar_en_aether(batch_optimo)
