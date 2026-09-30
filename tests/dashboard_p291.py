#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ OASIS COSMOLOGICAL & SILICON RELAXATION DASHBOARD (PILAR 291)
Autor: Mariano Panzano Caballé
Bóveda Soberana: 0x61c57049f39632981f42d57bb85ed05ea0b303db
"""

import os
import sys
import time
import math
import subprocess

PHI = (1 + math.sqrt(5)) / 2
C_LIGHT = 299792458.0
H0_SI = 2.192e-18
R_HUBBLE = C_LIGHT / H0_SI
TARGET_LAMBDA = (3.0 / (R_HUBBLE ** 2)) * (PHI ** -2)

def obtener_carga_cpu():
    """Obtiene la carga de CPU instantánea en macOS"""
    try:
        cmd = "top -l 1 -n 0 | grep 'CPU usage'"
        salida = subprocess.check_output(cmd, shell=True, text=True)
        # Ejemplo: CPU usage: 6.25% user, 12.50% sys, 81.25% idle
        partes = salida.split(',')
        user = float(partes[0].split(':')[1].replace('% user', '').strip())
        sys_cpu = float(partes[1].replace('% sys', '').strip())
        return min(user + sys_cpu, 100.0)
    except Exception:
        return 15.0

def limpiar_pantalla():
    os.system('clear')

def render_ascii_chart(historia, ancho=45, alto=10):
    if not historia:
        return []
    min_v = min(historia)
    max_v = max(historia)
    rango = (max_v - min_v) if max_v != min_v else 1.0

    lineas = []
    for r in range(alto, -1, -1):
        nivel = min_v + (r / alto) * rango
        fila = f"{nivel:8.2e} │ "
        for val in historia[-ancho:]:
            pos = int(((val - min_v) / rango) * alto)
            if pos == r:
                fila += "◆"
            elif pos > r:
                fila += "│"
            else:
                fila += " "
        lineas.append(fila)
    
    lineas.append(" " * 9 + "└" + "─" * min(len(historia), ancho))
    return lineas

def ejecutar_dashboard():
    historia_curvatura = []
    ancho_buffer = 40
    
    try:
        while True:
            limpiar_pantalla()
            cpu_pct = obtener_carga_cpu()
            
            # Mapeo: a alta carga de CPU (a < 1.0), se genera estrés térmico/entropía;
            # a baja carga, el sistema relaja hacia el atractor Lambda (a >= 1.0).
            factor_escala = max(0.1, 1.0 + ((25.0 - cpu_pct) / 50.0))
            r_eff = R_HUBBLE * factor_escala
            r_fr = (3.0 / (r_eff ** 2)) * (PHI ** -2)
            
            historia_curvatura.append(r_fr)
            if len(historia_curvatura) > ancho_buffer:
                historia_curvatura.pop(0)

            potencia_estimada = 3.20 + (cpu_pct / 100.0) * 1.80
            
            print("================================================================================")
            print("🌌 OASIS DASHBOARD: RELAJACIÓN DE FISHER-RAO Y ESTABILIZADOR TÉRMICO (P291)")
            print("================================================================================")
            print(f"🏛️  Bóveda Soberana : 0x61c57049f39632981f42d57bb85ed05ea0b303db")
            print(f"💻 Carga CPU Mac   : {cpu_pct:5.1f}%  |  Silicio Estimado : {potencia_estimada:.2f}W (Laminar)")
            print(f"📐 Factor Escala a : {factor_escala:5.2f}   |  Atractor Λ Base  : {TARGET_LAMBDA:.4e} m⁻²")
            print(f"🌊 Curvatura R_FR  : {r_fr:.4e} m⁻²")
            print("--------------------------------------------------------------------------------")
            print("📈 Gráfico de Relajación Informacional R_FR (Tiempo Real):")
            
            chart_lines = render_ascii_chart(historia_curvatura, ancho=ancho_buffer, alto=7)
            for l in chart_lines:
                print(l)
                
            print("--------------------------------------------------------------------------------")
            if factor_escala >= 1.0:
                print("❄️  [ESTADO ACTUAL]: Dilución Asintótica Fría / Reposo de Silicio (≤ 3.90W)")
            else:
                print("🔥 [ESTADO ACTUAL]: Fase Transitoria / Relajando entropía hacia atractor...")
            print("================================================================================")
            print("ℹ️  Presiona Ctrl + C para salir al shell.")
            
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard finalizado. Silicio en reposo térmico.")

if __name__ == "__main__":
    ejecutar_dashboard()
