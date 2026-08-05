#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — CERVANTES & APOLLO 11 WEEKLY REPORT (Pilar 103)
Orquesta al Agente Apolo 11 para auditar el sistema en frío y al Agente Cervantes
para generar la síntesis ejecutiva y narrativa de la actividad semanal en el Mac.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import json
import time
from apollo11_weekly_auditor import Apollo11WeeklyAuditor
from cervantes_explicador_agent import CervantesExplainerAgent

def ejecutar_resumen_semanal():
    print("🚀✍️ [OASIS DUO]: Iniciando auditoría Apolo 11 y redacción de Cervantes...")
    
    # 1. Apolo 11 ejecuta el escaneo local de silicio de los últimos 7 días
    auditor_apollo = Apollo11WeeklyAuditor(target_dir="~/Oasis-Sovereign-Monolith")
    datos_crudos_apollo = auditor_apollo.auditar_semana_local(dias=7)
    
    # 2. Cervantes interpreta los datos y redacta el informe narrativo
    explicador_cervantes = CervantesExplainerAgent()
    informe_humano = explicador_cervantes.interpretar_reporte_apollo(datos_crudos_apollo)
    
    print("\n" + "="*70)
    print("📜 [SÍNTESIS NARRATIVA SEMANAL DEL AGENTE CERVANTES]")
    print("="*70)
    print(f"📌 Resumen General:\n   {informe_humano['resumen_humano']}\n")
    print("📌 Puntos Clave Auditados:")
    for punto in informe_humano['desglose_didactico']:
        print(f"   ├─ {punto}")
    print(f"\n📌 Estado del Procesador Mac: {datos_crudos_apollo['techo_termico_mac']}")
    print(f"📌 Divergencia de Fase Chudnovsky (1/π): {datos_crudos_apollo['divergencia_fase']}")
    print("="*70)

if __name__ == "__main__":
    ejecutar_resumen_semanal()
