import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def __():
    import json
    import time
    from pathlib import Path
    import networkx as nx

    print("🌌 [OASIS MARIMO AUTOMATON]: Cuaderno Reactivo de Capa 0 Inicializado.")
    return Path, json, nx, time


@app.cell
def __(json, Path):
    # Celda Reactiva 1: Carga el Grafo de Conocimiento Graphify
    grafo_path = Path("data/lincos_db/oasis_knowledge_graph.json")
    total_nodos = 0
    if grafo_path.exists():
        with open(grafo_path, "r", encoding="utf-8") as f:
            data_graph = json.load(f)
            total_nodos = len(data_graph.get("nodes", []))
    print(f"🕸️ Nodos Activos en Graphify: {total_nodos}")
    return data_graph, grafo_path, total_nodos


@app.cell
def __(total_nodos):
    # Celda Reactiva 2: Estado del Autómata Térmico
    potencia_estimada = 3.90 + (total_nodos * 0.01)
    techo_ok = potencia_estimada <= 5.39
    dictamen = {
        "estado_automata": "LAMINAR ACTIVE",
        "potencia_watts": round(potencia_estimada, 2),
        "techo_5.39W_respetado": techo_ok
    }
    print(f"📊 Dictamen Térmico: {dictamen}")
    return dictamen, potencia_estimada, techo_ok


if __name__ == "__main__":
    app.run()
