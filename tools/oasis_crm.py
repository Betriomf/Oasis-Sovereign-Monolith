#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — CRM TÉCNICO Y AUDITOR DE ARQUITECTURA (v2.0)
Almacena métricas de silicio, comandos por versión, pilares e incidencias.
"""
import os
import sys
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_JSON = os.path.join(BASE_DIR, "vault", "crm_arquitectura_soberana.json")
CRM_MD = os.path.join(BASE_DIR, "vault", "bitacora_arquitectura_crm.md")

DEFAULT_DATABASE = [
    {
        "version": "v1.0.0 - v1.3.1",
        "tag_git": "v1.0-genesis",
        "fecha": "2026-03-04",
        "tecnologias": ["Python C-API", "Lean 4", "Zenodo DOI", "OpenTimestamps"],
        "comandos": ["falsability_test.py", "scale_test.f90", "scheduling_logic.lisp"],
        "pilares_asociados": [1, 2, 3, 18],
        "telemetria": {"potencia_w": 3.78, "latencia_ms": 120.0, "jitter_ms": 14.5},
        "hito_objetivo": "Génesis del Monolito: Formulación de Navier-Stokes y cota Landauer (+30.58%).",
        "que_funciono": ["Cierre analítico BKM", "Confinamiento enstrofía kappa = ln 10", "Auditoría formal sorry=0"],
        "errores_y_fallos": [
            {"sintoma": "Lentitud en cálculo tensorial en Python", "causa_raiz": "Sobrecarga de GIL y tipos dinámicos", "solucion_diseno": "Migración hacia C99 puro a nivel de registro"}
        ]
    },
    {
        "version": "v3.x - v7.x",
        "tag_git": "v7.1.0-sovereign-universal",
        "fecha": "2026-06-12",
        "tecnologias": ["VFS en RAM", "LocalStorage", "WASM Extism", "Isomorphic Git"],
        "comandos": ["help", "uname", "ls", "dir", "cat", "touch", "write", "rm", "lean", "ai", "caps"],
        "pilares_asociados": [14, 28, 46],
        "telemetria": {"potencia_w": 3.50, "latencia_ms": 15.0, "jitter_ms": 8.2},
        "hito_objetivo": "Micronúcleo en navegador con comandos POSIX y verificación formal temprana.",
        "que_funciono": ["Comandos ls/cat/uname en memoria", "Aislamiento Zero-Trust en WebAssembly"],
        "errores_y_fallos": [
            {"sintoma": "QuotaExceededError (> 5 MB)", "causa_raiz": "LocalStorage limitado a 5 MB por origen", "solucion_diseno": "Migración planificada hacia OPFS"}
        ]
    },
    {
        "version": "v15.x - v18.x",
        "tag_git": "v18.9.14-rag-sse",
        "fecha": "2026-09-20",
        "tecnologias": ["OPFS SyncAccessHandle", "WebCrypto AES-GCM", "O-QUIC", "Pacing Áureo (pi/phi)", "Three.js 3D"],
        "comandos": ["boveda", "box status", "mail", "quantum-run", "git-audit", "swarm", "hex-monitor", "yield"],
        "pilares_asociados": [14, 24, 47, 125],
        "telemetria": {"potencia_w": 3.71, "latencia_ms": 2.1, "jitter_ms": 0.085},
        "hito_objetivo": "Bóveda privada de alta velocidad y transporte P2P sin bufferbloat.",
        "que_funciono": ["I/O en RAM volátil < 0.12 ms", "Jitter colapsado a < 0.085 ms con cadencia de 1.938 ms"],
        "errores_y_fallos": [
            {"sintoma": "Bloqueo por Cross-Origin en recargas", "causa_raiz": "Cabeceras COOP/COEP malformadas", "solucion_diseno": "Estandarización de cabeceras no-store en Gateway"}
        ]
    },
    {
        "version": "v19.7 - v19.9",
        "tag_git": "v19.9.1-DualXterm-C99",
        "fecha": "2026-11-04",
        "tecnologias": ["DualXterm.js", "Python HTTP Gateway :8080", "C99 SIMD", "SOAP Protocol", "LINCOS 21B"],
        "comandos": ["v <pregunta>", "c99", "riona", "hemo", "lean_audit", "skills run", "view"],
        "pilares_asociados": [376, 378, 380, 382, 384],
        "telemetria": {"potencia_w": 3.73, "latencia_ms": 0.005, "jitter_ms": 0.017},
        "hito_objetivo": "Desacoplamiento táctico en dos paneles (Kernel Soberano vs DevFrame Darwin).",
        "que_funciono": ["Inferencia C99 en 0.005 ms", "Telemetría clínica vascular confinado a 3.73W", "LINCOS en 21 bytes"],
        "errores_y_fallos": [
            {"sintoma": "Cmd+V secuestrado por Xterm", "causa_raiz": "attachCustomKeyEventHandler interceptaba keydown", "solucion_diseno": "Manejador nativo de paste sobre window"},
            {"sintoma": "Git pre-push rechazaba archivos CRLF", "causa_raiz": "Conversión CRLF/LF en macOS", "solucion_diseno": "git config core.autocrlf false"}
        ]
    },
    {
        "version": "v20.0.0 - v20.0.5",
        "tag_git": "v20.0.5-dualxterm-stable",
        "fecha": "2026-11-10",
        "tecnologias": ["Ollama qwen:flash", "Micro-DHCP DORA C99", "Aduana Hashes SHA-256", "WebGL Addon"],
        "comandos": ["v", "c99", "boveda", "skills run (pacing_c99, soap_triage, lincos_radio, mesh, qr, id, crm)"],
        "pilares_asociados": [378, 384, 385, 386],
        "telemetria": {"potencia_w": 2.58, "latencia_ms": 0.005, "jitter_ms": 0.0001},
        "hito_objetivo": "Silicio frío estabilizado (2 hilos físicos), aduana de contenidos y Render deploy.",
        "que_funciono": ["Package power bajó a 2.58W en i5-8210Y", "Despliegue verificado en Render (200 OK)", "Puntero AdS/CFT .holo de 742 bytes"],
        "errores_y_fallos": [
            {"sintoma": "no space left on device", "causa_raiz": "Descarga de GLM 9B (5.96 GB) saturando SSD con solo 7.5 GB libres", "solucion_diseno": "Purga de blobs y fijación de qwen:flash a 397 MB"},
            {"sintoma": "Velázquez respondía con Pilar 378 a preguntas generales", "causa_raiz": "Llamada estricta a aether:fast que arrojaba 404 en Ollama", "solucion_diseno": "Cascada dinámica a qwen:flash"}
        ]
    }
]

def load_crm():
    if not os.path.exists(CRM_JSON):
        os.makedirs(os.path.dirname(CRM_JSON), exist_ok=True)
        with open(CRM_JSON, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATABASE, f, indent=2, ensure_ascii=False)
        return DEFAULT_DATABASE
    try:
        with open(CRM_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATABASE

def save_crm(data):
    with open(CRM_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Sincronización Markdown para la Bóveda E2EE
    with open(CRM_MD, "w", encoding="utf-8") as f:
        f.write("# 🏛️ OASIS SOVEREIGN OS — CRM TÉCNICO Y BITÁCORA ARQUITECTÓNICA LOCAL\n\n")
        f.write("> Registro inmutable de evolución de software, comandos por versión y física térmica en silicio frío.\n\n")
        
        # Tabla resumen de comandos y telemetría
        f.write("## 📊 MATRIZ COMPARATIVA DE TELEMETRÍA Y COMANDOS\n\n")
        f.write("| Versión | Potencia (W) | Latencia C99 | Jitter P99 | Pilares Mapeados | Comandos Clave |\n")
        f.write("| :--- | :---: | :---: | :---: | :--- | :--- |\n")
        for item in data:
            tel = item.get("telemetria", {})
            pils = ", ".join(str(p) for p in item.get("pilares_asociados", []))
            cmds = ", ".join(item.get("comandos", [])[:3]) + "..."
            f.write(f"| **{item['version']}** | `{tel.get('potencia_w', 3.78)} W` | `{tel.get('latencia_ms', 0)} ms` | `{tel.get('jitter_ms', 0)} ms` | {pils} | `{cmds}` |\n")
        f.write("\n---\n\n")

        for item in data:
            f.write(f"## 📦 {item['version']} | Tag: `{item['tag_git']}`\n")
            tel = item.get("telemetria", {})
            f.write(f"- **Fecha:** {item['fecha']} | **Potencia Silicio:** `{tel.get('potencia_w', 3.78)} W` | **Latencia:** `{tel.get('latencia_ms', 0)} ms`\n")
            f.write(f"- **Tecnologías:** {', '.join(item['tecnologias'])}\n")
            f.write(f"- **Comandos Activos:** `{', '.join(item.get('comandos', []))}`\n")
            f.write(f"- **Pilares Asociados:** `{', '.join(str(p) for p in item.get('pilares_asociados', []))}`\n")
            f.write(f"- **Hito:** {item['hito_objetivo']}\n")
            f.write("### ✅ Qué Funcionó:\n")
            for w in item["que_funciono"]:
                f.write(f"  - {w}\n")
            f.write("### ⚠️ Errores Reportados y Solución de Diseño:\n")
            for err in item["errores_y_fallos"]:
                f.write(f"  - **Error:** `{err['sintoma']}`\n")
                f.write(f"    - *Causa Raíz:* {err['causa_raiz']}\n")
                f.write(f"    - *Decisión:* {err['solucion_diseno']}\n")
            f.write("\n---\n\n")

def record_incident(version, error_text, causa, solucion):
    data = load_crm()
    updated = False
    for item in data:
        if version.lower() in item["version"].lower():
            item["errores_y_fallos"].append({
                "sintoma": error_text,
                "causa_raiz": causa,
                "solucion_diseno": solucion
            })
            updated = True
            break
    if not updated:
        # Añadir a la última versión
        data[-1]["errores_y_fallos"].append({
            "sintoma": error_text,
            "causa_raiz": causa,
            "solucion_diseno": solucion
        })
    save_crm(data)
    print(f"✅ Incidencia registrada en versión {version}.")

def list_versions():
    data = load_crm()
    print("════════════════════════════════════════════════════════════════")
    print("📜 OASIS CRM LOCAL — HISTORIAL TÉCNICO Y COMANDOS")
    print("────────────────────────────────────────────────────────────────")
    for idx, item in enumerate(data, 1):
        tel = item.get("telemetria", {})
        print(f"{idx}. {item['version']:<18} | Tag: {item['tag_git']:<22} | {tel.get('potencia_w', 3.78)} W")
        print(f"   Cmds   : {', '.join(item.get('comandos', [])[:5])}...")
        print(f"   Pilares: {', '.join(str(p) for p in item.get('pilares_asociados', []))}")
        print(f"   Hito   : {item['hito_objetivo'][:65]}...")
        print("────────────────────────────────────────────────────────────────")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        list_versions()
    elif sys.argv[1] == "sync":
        data = load_crm()
        save_crm(data)
        print("✅ Bitácora Markdown y JSON sincronizados con éxito.")
    elif sys.argv[1] == "incident" and len(sys.argv) >= 5:
        # Uso: python3 tools/oasis_crm.py incident <version> <error> <causa> <solucion>
        record_incident(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("Uso: python3 tools/oasis_crm.py <list | sync | incident <version> <error> <causa> <solucion>>")

if __name__ == "__main__":
    main()
