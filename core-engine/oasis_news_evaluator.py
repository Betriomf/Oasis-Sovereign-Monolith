#!/usr/bin/env python3
import json
import math
import subprocess

class OasisThermodynamicEvaluator:
    def __init__(self, model_name: str = "qwen2.5-oasis-oasis-oasis"):
        self.model_name = model_name
        self.k_alpha = 0.07  # Constante de acoplamiento Oasis

    def calculate_shannon_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
        total = len(text)
        return -sum((count / total) * math.log2(count / total) for count in frequencies.values())

    def query_oasis_model(self, prompt: str) -> str:
        """Consulta el modelo local optimizado usando la CLI de Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error en inferencia local: {str(e)}"

    def evaluate_news(self, news_content: str) -> dict:
        h_info = self.calculate_shannon_entropy(news_content)
        
        # Generar prompt formal bajo principios de PAPER_THERMODYNAMICS
        prompt = (
            f"Analiza la siguiente noticia bajo un criterio de innovación real frente a humo tecnológico. "
            f"Responde en un párrafo corto y conciso.\nNoticia: {news_content}"
        )
        
        model_response = self.query_oasis_model(prompt)
        
        contains_miracle = "milagrosa" in news_content.lower() or "sin cambiar" in news_content.lower()
        dissipation_risk = 0.95 if contains_miracle else 0.15
        efficiency = (1 - dissipation_risk) * (1 - self.k_alpha)

        return {
            "status": "STRATEGIC_VAL_CLOSED",
            "metrics": {
                "shannon_entropy_bits": round(h_info, 4),
                "dissipation_risk": dissipation_risk,
                "thermodynamic_efficiency": round(efficiency, 4)
            },
            "model_analysis": model_response,
            "actionable": efficiency > 0.50
        }

if __name__ == "__main__":
    evaluator = OasisThermodynamicEvaluator()
    test_news = "Empresa de software lanza solución milagrosa de IA sin cambiar la estructura organizativa de sus clientes."
    print("\n[OASIS CORE] Ejecutando análisis termo-estratégico de prueba...\n")
    report = evaluator.evaluate_news(test_news)
    print(json.dumps(report, indent=2, ensure_ascii=False))
