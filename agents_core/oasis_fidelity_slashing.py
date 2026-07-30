#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — QUANTUM FIDELITY & SLASHING ENGINE (Pilar 35)
Motor de Gobernanza e Inmunidad:
1. Medición de Fidelidad Cuántica (F) contra Data Poisoning.
2. Ejecución de Slashing (incautación de Staking $SPN) a nodos Sybil/Spoofing.
3. Actualización de reputación en la Malla Hexagonal (√3).

Autor: Mariano Panzano Caballé (@Betriomf)
"""

import math
import time

FIDELITY_THRESHOLD = 0.90 # Umbral mínimo de coherencia de información

class OasisFidelitySlashingEngine:
    def __init__(self):
        print("⚖️ [FIDELITY & SLASHING ENGINE]: Inicializando Tribunal Algorítmico...")

    def calcular_fidelidad_cuantica(self, vector_original: list, vector_actualizado: list) -> float:
        """
        Calcula la Fidelidad Cuántica F = |<ψ|φ>|^2 entre el estado base y el recibido.
        """
        dot_product = sum(a * b for a, b in zip(vector_original, vector_actualizado))
        norm_a = math.sqrt(sum(a ** 2 for a in vector_original))
        norm_b = math.sqrt(sum(b ** 2 for b in vector_actualizado))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        fidelidad = (dot_product / (norm_a * norm_b)) ** 2
        return fidelidad

    def auditar_nodo_y_ejecutar_slashing(self, id_nodo: str, staking_spn: float, vector_base: list, vector_recibido: list, brownian_ok: bool):
        print(f"\n🔍 [AUDITORÍA DE NODO]: Inspeccionando '{id_nodo}' (Staking: {staking_spn:.2f} $SPN)")
        print("-" * 65)

        # 1. Verificar Entropía Browniana
        if not brownian_ok:
            print(" 🚨 [ALERTA SYBIL]: Tráfico uniforme/sintético detectado sin ruido browniano.")
            print(f" 💥 [SLASHING EJECUTADO]: Incautados {staking_spn:.2f} $SPN. Reputación revocada.")
            return {"status": "SLASHED", "reason": "Sybil Botnet Brownian Failure", "penalty_spn": staking_spn}

        # 2. Verificar Fidelidad Cuántica
        fidelidad = self.calcular_fidelidad_cuantica(vector_base, vector_recibido)
        print(f" ├─ Fidelidad Cuántica de Información (F): {fidelidad:.4f}")

        if fidelidad < FIDELITY_THRESHOLD:
            penalty = staking_spn * 0.50 # Slashing del 50% por Data Poisoning
            print(f" ⚠️ [DATA POISONING DETECTADO]: Fidelidad {fidelidad:.4f} < {FIDELITY_THRESHOLD}.")
            print(f" 💥 [SLASHING PARCIAL]: Penalización de {penalty:.2f} $SPN aplicada.")
            return {"status": "PARTIAL_SLASH", "reason": "Data Poisoning / Low Fidelity", "penalty_spn": penalty}

        print(" ✅ [NODO INTEGRAL]: Transacción válida. Incrementando reputación en Malla Hexagonal.")
        return {"status": "CLEAN", "fidelidad": fidelidad}

if __name__ == "__main__":
    engine = OasisFidelitySlashingEngine()
    
    # Datos de referencia (Vector latente base)
    vector_base = [0.1059, 1.6180, 2.3025, 0.5540]
    
    # Caso 1: Actualización Legítima de Alta Fidelidad
    vector_valido = [0.1060, 1.6179, 2.3026, 0.5539]
    engine.auditar_nodo_y_ejecutar_slashing("NODO_BARCELONA_HONESTO", staking_spn=100.0, vector_base=vector_base, vector_recibido=vector_valido, brownian_ok=True)
    
    # Caso 2: Intento de Data Poisoning (Inyección de Basura)
    vector_veneno = [0.9999, 0.0001, 9.9999, 0.1111]
    engine.auditar_nodo_y_ejecutar_slashing("NODO_POISONER_01", staking_spn=100.0, vector_base=vector_base, vector_recibido=vector_veneno, brownian_ok=True)

    # Caso 3: Granja Sybil Sintética (Fallo Browniano)
    engine.auditar_nodo_y_ejecutar_slashing("BOTNET_SYBIL_FARM", staking_spn=250.0, vector_base=vector_base, vector_recibido=vector_valido, brownian_ok=False)
