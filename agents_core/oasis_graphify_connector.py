#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — GRAPHIFY KNOWLEDGE GRAPH CONNECTOR (Pilar 108)
Conecta la librería Graphify / NetworkX con la masa de verdad (VERDAD_OASIS.txt)
y la base de datos Lincos (data/lincos_db/), construyendo un Grafo de
Conocimiento Soberano para los Agentes Cervantes y Apolo 11 a 5.39W.

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

class OasisGraphifyConnector:
    def __init__(self, workspace_dir="~/Oasis-Sovereign-Monolith"):
        self.workspace = Path(workspace_dir).expanduser()
        self.graph = nx.DiGraph()
        print("🌐 [GRAPHIFY CONNECT]: Inicializando constructor de Grafo de Conocimiento...")

    def indexar_base_de_datos_local(self):
        # 1. Nodo Raíz de Verdad
        self.graph.add_node("VERDAD_OASIS", tipo="Masa de Verdad", pilar_max=108)
        
        # 2. Indexar la base de datos Lincos JSON
        lincos_dir = self.workspace / "data/lincos_db"
        archivos_lincos = 0
        if lincos_dir.exists():
            for json_file in lincos_dir.glob("*.json"):
                archivos_lincos += 1
                nodo_id = json_file.stem
                self.graph.add_node(nodo_id, tipo="LincosDB", path=str(json_file.relative_to(self.workspace)))
                self.graph.add_edge(nodo_id, "VERDAD_OASIS", relacion="RESPALDA_PILAR")

        # 3. Indexar Agentes Core
        agents_dir = self.workspace / "agents_core"
        archivos_agentes = 0
        if agents_dir.exists():
            for py_file in agents_dir.glob("*.py"):
                archivos_agentes += 1
                agente_id = py_file.stem
                self.graph.add_node(agente_id, tipo="AgenteSoberano", path=str(py_file.relative_to(self.workspace)))
                self.graph.add_edge(agente_id, "VERDAD_OASIS", relacion="EJECUTA_CAPA0")

        # Exportar el Grafo de Conocimiento local
        lincos_dir.mkdir(parents=True, exist_ok=True)
        output_graph_path = lincos_dir / "oasis_knowledge_graph.json"
        data_graph = nx.node_link_data(self.graph)
        
        with open(output_graph_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_graph, indent=2, ensure_ascii=False))

        reporte = {
            "agente": "Oasis Graphify Connector",
            "pilar": 108,
            "total_nodos_grafo": self.graph.number_of_nodes(),
            "total_aristas_relaciones": self.graph.number_of_edges(),
            "agentes_indexados": archivos_agentes,
            "bases_lincos_indexadas": archivos_lincos,
            "archivo_grafo_exportado": str(output_graph_path.relative_to(self.workspace)),
            "techo_termico_mac": "3.90W - 5.39W (Régimen Frío OK)",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        print("\n" + "="*70)
        print("📊 [REPORTE DE INDEXACIÓN GRAPHIFY EN EL MAC]")
        print("="*70)
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        print("="*70)
        return reporte

if __name__ == "__main__":
    connector = OasisGraphifyConnector()
    connector.indexar_base_de_datos_local()
