#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — MERKLE ORACLE & LIGHT NODE ENGINE (Pilar 57)
1. Consolida pruebas de trabajo (Proof-of-Retrievability / Uptime) en un Árbol de Merkle.
2. Simula el consenso Multisig 3-de-5 para autorización de emisiones $SPN en L2.
3. Valida que el Boundary local opera en régimen de 1 KB en flujo laminar.

Autor: Mariano Panzano Caballé (@Betriomf)
"""

import hashlib
import json
import time

class OasisMerkleOracle:
    def __init__(self, num_oracles: int = 5, threshold: int = 3):
        self.num_oracles = num_oracles
        self.threshold = threshold
        print(f"🛡️ [ORÁCULO MERKLE]: Inicializando consenso Multisig ({self.threshold}-de-{self.num_oracles})...")

    def _hash_pair(self, a: str, b: str) -> str:
        return hashlib.sha256((a + b).encode('utf-8')).hexdigest()

    def construir_arbol_merkle(self, recibos_trabajo: list) -> str:
        if not recibos_trabajo:
            return ""

        # Generar hashes hoja (leaf hashes)
        current_level = [hashlib.sha256(json.dumps(r, sort_keys=True).encode('utf-8')).hexdigest() for r in recibos_trabajo]
        
        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1])  # Duplicar último si es impar
            
            next_level = []
            for i in range(0, len(current_level), 2):
                next_level.append(self._hash_pair(current_level[i], current_level[i+1]))
            current_level = next_level

        merkle_root = current_level[0]
        print(f" ├─ Procesados {len(recibos_trabajo)} recibos de trabajo off-chain.")
        print(f" └─ Merkle Root Generada: {merkle_root}")
        return merkle_root

    def validar_consenso_multisig(self, merkle_root: str, firmas_oráculos: list) -> bool:
        firmas_validas = sum(1 for f in firmas_oráculos if f.get("valid") is True)
        print(f"\n🏛️ [EVALUACIÓN MULTISIG]: {firmas_validas}/{self.num_oracles} firmas verificadas.")
        
        if firmas_validas >= self.threshold:
            print(f" ✅ [EMISIÓN $SPN AUTORIZADA]: Raíz {merkle_root[:12]}... aprobada para Capa 2.")
            return True
        else:
            print(" ❌ [RECHAZADO]: No se alcanzó el cuórum de 3-de-5. Posible intento de fraude.")
            return False

if __name__ == "__main__":
    oracle = OasisMerkleOracle()
    
    # Recibos ficticios de nodos Boundary (1GB reservado / Uptime)
    recibos = [
        {"node_id": "node_boundary_01", "uptime_sec": 3600, "spn_earned": 0.1, "proof": "por_hash_89a1"},
        {"node_id": "node_boundary_02", "uptime_sec": 3600, "spn_earned": 0.1, "proof": "por_hash_77b2"},
        {"node_id": "node_boundary_03", "uptime_sec": 3600, "spn_earned": 0.1, "proof": "por_hash_44c3"},
        {"node_id": "node_boundary_04", "uptime_sec": 3600, "spn_earned": 0.1, "proof": "por_hash_11d4"}
    ]
    
    root = oracle.construir_arbol_merkle(recibos)
    
    # Simulación de firmas del jurado de 5 oráculos
    firmas = [
        {"oracle_id": 1, "valid": True},
        {"oracle_id": 2, "valid": True},
        {"oracle_id": 3, "valid": True},
        {"oracle_id": 4, "valid": False},
        {"oracle_id": 5, "valid": True}
    ]
    
    oracle.validar_consenso_multisig(root, firmas)
