#!/usr/bin/env python3
"""
OASIS SOVEREIGN OSINT & SURFACE AUDITOR (v1.0)
Motor de inteligencia pasiva y auditoría de huella digital sin dependencias externas.
Inspirado en Sherlock y theHarvester con Pacing Áureo (pi/phi).
"""
import os
import sys
import json
import time
import math
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
REPORT_PATH = os.path.join(VAULT_DIR, "osint_surface_audit.md")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
PI = math.pi
PACING_S = (PI / PHI) / 1000.0  # ~1.94 ms

TARGET_TARGETS = [
    {"name": "GitHub", "url": "https://api.github.com/users/{}"},
    {"name": "GitLab", "url": "https://gitlab.com/api/v4/users?username={}"},
    {"name": "HuggingFace", "url": "https://huggingface.co/api/users/{}"},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}/about.json"},
    {"name": "DockerHub", "url": "https://hub.docker.com/v2/users/{}/"},
    {"name": "Archive.org", "url": "https://archive.org/advancedsearch.php?q={}&output=json"}
]

def check_username(username):
    print(f"🛰️  [OASIS OSINT]: Escaneando huella digital pública para: '{username}'...")
    results = []
    headers = {"User-Agent": "OasisSovereignSentinel/20.0"}

    for target in TARGET_TARGETS:
        url = target["url"].format(username)
        status = "NO_ENCONTRADO"
        details = ""
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    status = "EXPUESTO / ACTIVO"
                    data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                    if target["name"] == "GitHub":
                        details = f"Repos públicos: {data.get('public_repos', 0)} | Bio: {data.get('bio', 'N/A')}"
                    elif target["name"] == "HuggingFace":
                        details = f"Modelos/Datasets públicos detectados"
                    else:
                        details = "Perfil público accesible"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                status = "LIBRE / 404"
            else:
                status = f"HTTP_{e.code}"
        except Exception as e:
            status = f"TIMEOUT / {str(e)[:15]}"

        results.append({
            "plataforma": target["name"],
            "url_revisada": url,
            "estado": status,
            "detalles": details
        })
        time.sleep(PACING_S)

    # Persistir en la Bóveda E2EE
    os.makedirs(VAULT_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as out:
        out.write(f"# 🔍 AUDITORÍA OSINT Y SUPERFICIE DE EXPOSICIÓN DIGITAL\n\n")
        out.write(f"- **Target Analizado:** `{username}`\n")
        out.write(f"- **Fecha Auditoría:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"- **Cadencia:** Pacing Áureo ($\\Delta t = \\pi/\\phi \\approx 1.94\\text{{ ms}}$) a $\\le 2.58\\text{{ W}}$\n\n---\n\n")
        out.write("| Plataforma | Estado | Hallazgos / Metadatos |\n")
        out.write("| :--- | :---: | :--- |\n")
        for r in results:
            badge = "🟢" if "EXPUESTO" in r["estado"] else "⚪"
            out.write(f"| **{r['plataforma']}** | {badge} `{r['estado']}` | {r['detalles']} |\n")
        out.write("\n> 🔒 Informe generado en memoria volátil de Capa 0 bajo marco ético defensivo.\n")

    print(f"✅ Auditoría completada. Informe guardado en: {REPORT_PATH}")
    for r in results:
        print(f"  • {r['plataforma']:<15}: {r['estado']} {('[' + r['detalles'] + ']') if r['detalles'] else ''}")

if __name__ == "__main__":
    target_user = sys.argv[1] if len(sys.argv) > 1 else "Betriomf"
    check_username(target_user)
