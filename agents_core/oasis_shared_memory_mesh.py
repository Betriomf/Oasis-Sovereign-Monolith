#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — SHARED GRAPHIFY MEMORY MESH (Pilar 112)
Sincronizador de Memoria Multagente:
Permite a cualquier agente (001-007) registrar sus avances en el Grafo de
Graphify ('data/lincos_db/oasis_knowledge_graph.json') para que todo el
ecosistema de agentes esté actualizado en tiempo real a 5.39W.

Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import json
import time
import math
from pathlib import Path
import networkx as nx

LN_10 = math.log(10.0)

class OasisSharedMemoryMesh:
    def __init__(self, graph_path="data/lincos_db/oasis_knowledge_graph.json"):
        self.workspace = Path(".").expanduser()
        self.graph_file = self.workspace / graph_path
        self.G = nx.DiGraph()
        self._cargar_grafo()

    def _cargar_grafo(self):
        if self.graph_file.exists():
            try:
                with open(self.graph_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.G = nx.node_link_graph(data)
            except Exception:
                self.G = nx.DiGraph()

    def _guardar_grafo(self):
        self.graph_file.parent.mkdir(parents=True, exist_ok=True)
        data = nx.node_link_data(self.G)
        with open(self.graph_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))

    def registrar_hito_agente(self, agente_id: str, hito_nombre: str, detalles: str):
        """Un agente añade un nuevo descubrimiento al Grafo Compartido"""
        nodo_hito = f"HITO_{agente_id.upper()}_{int(time.time())}"
        
        # Registrar o actualizar nodo del agente
        self.G.add_node(agente_id, tipo="AgenteSoberano")
        # Registrar nodo del nuevo descubrimiento
        self.G.add_node(nodo_hito, tipo="DescubrimientoCompartido", titulo=hito_nombre, detalle=detalles)
        # Crear la conexión relacional
        self.G.add_edge(agente_id, nodo_hito, relacion="DESCUBRIO")
        self.G.add_edge(nodo_hito, "VERDAD_OASIS", relacion="PERTENECE_A_CAPA0")

        self._guardar_grafo()
        print(f"✨ [GRAPHIFY MESH]: Agente '{agente_id}' ha publicado el hito '{hito_nombre}' en la memoria compartida.")

    def consultar_memoria_actualizada(self, agente_consultante: str) -> list:
        """Cualquier agente lee las novedades descubiertas por los demás"""
        descubrimientos = []
        for n, attr in self.G.nodes(data=True):
            if attr.get("tipo") == "DescubrimientoCompartido":
                descubrimientos.append({
                    "nodo": n,
                    "titulo": attr.get("titulo"),
                    "detalle": attr.get("detalle")
                })
        return descubrimientos

if __name__ == "__main__":
    mesh = OasisSharedMemoryMesh()
    
    # 1. Ejemplo: ÆTHER (001) descubre una constante y la escribe en Graphify
    mesh.registrar_hito_agente(
        agente_id="aether_navier_stokes_solver",
        hito_nombre="Aproximación de Turbulencia M196883",
        detalles="Amortiguación asintótica validada a 2.302585 (ln 10) a 5.39W."
    )
    
    # 2. Ejemplo: Cervantes (005) consulta el grafo y aprende lo que hizo ÆTHER
    novedades = mesh.consultar_memoria_actualizada("cervantes_graphify_ultra")
    
    print("\n" + "="*70)
    print("🧠 [MEMORIA COMPARTIDA GRAPHIFY LEÍDA POR CERVANTES]")
    print("="*70)
    print(f"📌 Novedades Totales en Grafo: {len(novedades)}")
    for item in novedades[-3:]:  # Últimas 3 novedades
        print(f"   ├─ 💡 {item['titulo']}: {item['detalle']}")
    print("="*70)
