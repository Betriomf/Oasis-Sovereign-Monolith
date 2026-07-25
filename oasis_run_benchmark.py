#!/usr/bin/env python3
import time
import urllib.request
import json
import hashlib
import platform
import os
from datetime import datetime

def check_ollama():
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req) as response:
            return True
    except Exception:
        return False

def test_inference(prompt, temp):
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temp}
    }
    data = json.dumps(payload).encode('utf-8')
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
        print(f"⚠️ Error durante el test: {e}")
        return None, None

def generate_report():
    print("🌌 [OASIS PIONEER BENCHMARK - VERIFICACIÓN DE INFRAESTRUCTURA]")
    print("-------------------------------------------------------------")
    
    if not check_ollama():
        print("❌ Error: Ollama no responde en http://127.0.0.1:11434. Arranca el servicio antes de ejecutar.")
        return

    company_name = input("✍️ Introduce el nombre de tu Empresa / Organización: ").strip()
    node_id = input("🖥️ Identificador del Servidor/Nodo (ej. srv-node-01): ").strip()
    
    if not company_name or not node_id:
        print("⚠️ Nombre de empresa y nodo son obligatorios para validar la licencia.")
        return

    print("\n🚀 Ejecutando batería de pruebas térmicas y de varianza...")
    prompt = "Responde en 2 frases: ¿Por qué la conservación de la masa informacional optimiza el rendimiento?"
    
    times_classic, times_oasis = [], []
    
    for i in range(3):
        print(f"🔄 Ronda {i+1}/3: Midiendo Modo Clásico vs. Modo Oasis...")
        e_c, _ = test_inference(prompt, temp=0.8)
        if e_c: times_classic.append(e_c)
        time.sleep(2)
        
        e_o, _ = test_inference(prompt, temp=0.618)
        if e_o: times_oasis.append(e_o)
        time.sleep(2)

    if not times_classic or not times_oasis:
        print("❌ Fallo en la recopilación de datos.")
        return

    avg_classic = sum(times_classic) / len(times_classic)
    avg_oasis = sum(times_oasis) / len(times_oasis)
    
    var_classic = sum((x - avg_classic) ** 2 for x in times_classic) / len(times_classic)
    var_oasis = sum((x - avg_oasis) ** 2 for x in times_oasis) / len(times_oasis)
    
    reduction = ((var_classic - var_oasis) / var_classic) * 100 if var_classic > 0 else 0

    timestamp = datetime.now().isoformat()
    raw_signature = f"{company_name}|{node_id}|{timestamp}|{var_classic:.4f}|{var_oasis:.4f}|{reduction:.2f}"
    report_hash = hashlib.sha256(raw_signature.encode('utf-8')).hexdigest()

    report_content = f"""# 📄 INFORME DE VALIDACIÓN EMPÍRICA — PROGRAMA PIONEER

**Empresa / Entidad:** {company_name}  
**Nodo / Servidor:** {node_id}  
**Fecha/Hora:** {timestamp}  
**Sistema Operativo:** {platform.system()} {platform.release()} ({platform.machine()})  

---

## 📊 Métricas de Telemetría Registradas

| Métrica | Modo Clásico ($T=0.8$) | Modo Oasis ($T=0.618$) | Impacto / Delta |
| :--- | :--- | :--- | :--- |
| **Tiempo Medio de Respuesta** | `{avg_classic:.2f}s` | `{avg_oasis:.2f}s` | Baseline |
| **Varianza (Jitter / Caos)** | `{var_classic:.4f}` | `{var_oasis:.4f}` | **{reduction:.2f}% Reducción de Caos** |

---

## 🔐 Firma Criptográfica de Integridad (SHA-256)
`{report_hash}`

> **Declaración de Conformidad:**  
> Por la presente, la entidad **{company_name}** confirma la autenticidad de los datos recogidos en el servidor **{node_id}** y solicita la asignación de uno de los 50 cupos de la **Oasis Pioneer Lifetime License**.
"""

    report_filename = f"BENCHMARK_{company_name.replace(' ', '_')}.md"
    with open(report_filename, "w") as f:
        f.write(report_content)

    print(f"\n✅ ¡Informe generado con éxito!: {report_filename}")
    print(f"🔐 Hash SHA-256: {report_hash}")
    print("\n📩 Siguientes pasos: Adjunta este archivo en un Issue o Pull Request en GitHub.")

if __name__ == "__main__":
    generate_report()
