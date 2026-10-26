#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS HISTORICAL REVERSE-ENGINEERING INVENTORY
Inspecciona commits y tags históricos para catalogar comandos, modales y endpoints.
"""
import subprocess, re, json

def run_git(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

def get_tags():
    tags = run_git("git tag --sort=creatordate").splitlines()
    return [t.strip() for t in tags if t.strip()]

def inspect_tag(tag):
    html = run_git(f"git show {tag}:agents_core/templates/terminal.html 2>/dev/null")
    py = run_git(f"git show {tag}:agents_core/oasis_render_gateway.py 2>/dev/null")
    
    # 1. Endpoints en Python
    endpoints = sorted(list(set(re.findall(r'self\.path\s*==\s*["\'](/v1/[^"\']+)["\']', py) + 
                               re.findall(r'self\.path\.startswith\(["\'](/v1/[^"\']+)["\']', py))))
    
    # 2. Modales en HTML
    modals = sorted(list(set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+-modal)["\']', html))))
    
    # 3. Comandos en JavaScript (COMMAND_REGISTRY y bloques if)
    cmds_reg = re.findall(r'["\']([a-zA-Z0-9_\- ]+)["\']\s*:\s*\(\)', html)
    cmds_if = re.findall(r'low\s*===\s*["\']([^"\']+)["\']', html)
    cmds_starts = re.findall(r'low\.startsWith\(["\']([^"\']+)["\']', html)
    all_cmds = sorted(list(set(cmds_reg + cmds_if + cmds_starts)))
    
    # 4. Badges en cabecera
    badges = re.findall(r'<span[^>]*class=["\'][^"\']*badge[^"\']*["\'][^>]*>(.*?)</span>', html, re.DOTALL)
    clean_badges = [re.sub(r'<[^>]+>', '', b).strip() for b in badges if b.strip()]

    return {
        "tag": tag,
        "endpoints_count": len(endpoints),
        "endpoints": endpoints,
        "modals": modals,
        "commands_count": len(all_cmds),
        "commands": all_cmds[:12], # Primeros 12 para resumen
        "badges": clean_badges[:6]
    }

if __name__ == "__main__":
    tags = get_tags()
    print(f"📦 Analizando {len(tags)} versiones registradas en Git...\n")
    print(f"{'VERSIÓN':<26} | {'ENDPOINTS':<10} | {'COMANDOS':<10} | {'MODALES ACTIVOS'}")
    print("-" * 80)
    
    inventory = []
    for t in tags[-10:]: # Últimas 10 versiones para análisis comparativo
        data = inspect_tag(t)
        inventory.append(data)
        modals_str = ", ".join([m.replace("-modal", "") for m in data["modals"]])
        print(f"{data['tag']:<26} | {data['endpoints_count']:<10} | {data['commands_count']:<10} | {modals_str}")

    with open("INVENTARIO_OASIS_REVERSO.json", "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
    print("\n✅ Inventario técnico guardado en 'INVENTARIO_OASIS_REVERSO.json'.")
