# 🌌 COMPONENTE CUSTOM OASIS PARA LANGFLOW
# Copia este código dentro de un nodo "Custom Component" en la interfaz de Langflow

from langflow.custom import CustomComponent
from langflow.field_typing import Text
import math

class OasisRouterComponent(CustomComponent):
    display_name = "🌌 Oasis Metronomic Router"
    description = "Filtra inputs y enruta el flujo según el Atractor ln 10 (~2.3)."

    def build_config(self):
        return {
            "input_text": {"display_name": "Input Prompt (Capa 22)", "is_filter": True},
            "force_local": {"display_name": "Forzar Silicio Local (0.000)", "input_type": "boolean"},
        }

    def build(self, input_text: str, force_local: bool = False) -> str:
        PHI_O = 2.3026
        tokens_est = len(input_text.split())
        
        # Aduana de seguridad básica (Anti-inyección)
        if any(char in input_text for char in ["<script>", "DROP TABLE", "--"]):
            self.status = "🚨 Turbulencia detectada: Intento de inyección."
            return "RECHAZADO: Entrada no laminar."

        # Algoritmo de enrutamiento bajo el atractor
        if force_local or tokens_est < (PHI_O * 10):
            # Enruta al modelo local qwen2.5 de Ollama
            destino = "LOCAL_OLLAMA_QWEN"
            explicacion = f"Tamaño ({tokens_est} t) menor que el umbral exponencial. Procesamiento en frío absoluto."
        else:
            # Enruta a la Capa 1 de Gemini para contextos masivos
            destino = "CLOUD_GEMINI"
            explicacion = f"Volumen expansivo detectado. Requiere escalado a e-folds superiores."

        resultado_json = f'{{"target": "{destino}", "reason": "{explicacion}", "phi_calib": {PHI_O}}}'
        self.status = f"💎 Sincronización exitosa. Destino: {destino}"
        return resultado_json
