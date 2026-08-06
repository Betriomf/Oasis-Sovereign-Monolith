#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — AGENT IDEA SURVIVAL & PIVOT ENGINE (Pilar 115)
Evaluador de Supervivencia Económica de Ideas:
1. Analiza propuestas generadas por los Agentes (Cervantes, Riona, ÆTHER).
2. Modela la viabilidad económica frente al consumo térmico de 5.39W.
3. Clasifica la idea: REPLICAR (Clonar), PIVOTAR o ARCHIVAR.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import json
import time
import math
from pathlib import Path

LN_10 = math.log(10.0)

class OasisIdeaSurvivalEvaluator:
    def __init__(self):
        self.workspace = Path(".").expanduser()
        print("⚡ [SURVIVAL EVALUATOR]: Evaluando matriz de viabilidad económica de agentes...")

    def evaluar_propuestas(self, lista_ideas: list) -> dict:
        resultados = []
        for idea in lista_ideas:
            nombre = idea.get("nombre", "Idea Anónima")
            ingreso_estimado = idea.get("ingreso_mensual_est", 0.0)
            coste_computo = idea.get("coste_watts_est", 4.0) * 0.15  # Coste equivalente
            
            roi = ingreso_estimado - coste_computo
            
            if roi >= 50.0:
                dictamen = "REPLICAR (Clonar Agentes Dedicados)"
                accion = "Asignar sub-red de Ollama + Graphify"
            elif roi > 0.0:
                dictamen = "PIVOTAR (Optimizar Rendimiento)"
                accion = "Ajustar parámetros con Lincos y reducir coste"
            else:
                dictamen = "ARCHIVAR (Pérdida de Vitalidad)"
                accion = "Liberar RAM y congelar proceso en Grafo"

            resultados.append({
                "idea": nombre,
                "ingreso_est_eur": ingreso_estimado,
                "coste_computo_eur": round(coste_computo, 2),
                "roi_neto": round(roi, 2),
                "dictamen": dictamen,
                "accion_recomendada": accion
            })

        reporte = {
            "agente": "Oasis Survival & Pivot Engine",
            "pilar": 115,
            "ideas_evaluadas": len(resultados),
            "resultados_matriz": resultados,
            "techo_termico_mac": "3.90W - 5.39W (Silicio Frío OK)",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        print("\n" + "="*75)
        print("📊 [REPORTE DE SUPERVIVENCIA Y PIVOTAJE DE IDEAS — CAPA 0]")
        print("="*75)
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        print("="*75)
        return reporte

if __name__ == "__main__":
    evaluator = OasisIdeaSurvivalEvaluator()
    # Muestra de proyectos para evaluación
    proyectos_demo = [
        {"nombre": "SaaS Plegamiento Proteínas B2B", "ingreso_mensual_est": 1200.0, "coste_watts_est": 4.41},
        {"nombre": "API Consultas Lincos Genérica", "ingreso_mensual_est": 15.0, "coste_watts_est": 5.0},
        {"nombre": "Generador de Banners Spam", "ingreso_mensual_est": -5.0, "coste_watts_est": 5.39}
    ]
    evaluator.evaluar_propuestas(proyectos_demo)
