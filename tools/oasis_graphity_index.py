import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(".")
GRAPH_OUT = ROOT / "vault/oasis_graphity.json"

def build_graph() -> dict:
    nodes = {}
    edges = []

    def add_node(nid: str, ntype: str, summary: str, ref: str):
        nodes[nid] = {"id": nid, "type": ntype, "summary": summary[:260], "ref": ref}

    def add_edge(src: str, rel: str, dst: str):
        edges.append({"from": src, "rel": rel, "to": dst})

    # 1. Nodos de Papers y Pruebas Formales Lean 4
    for p in sorted(ROOT.glob("papers/paper_*.tex")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"\\title\{(.+?)\}", txt, re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else p.stem
        add_node(p.stem, "paper", title, str(p))

    for lf in sorted(ROOT.glob("formal_proofs/*.lean")):
        first_doc = ""
        for ln in lf.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = ln.strip()
            if s.startswith("Alcance:") or s.startswith("--"):
                first_doc = s.lstrip("- ").strip()
                break
        add_node(lf.stem, "lean4", first_doc or f"Módulo Lean 4 {lf.stem}", str(lf))

    # 2. Enlaces explícitos de la serie Y -> Z y Pilar 389
    add_node(
        "pilar_389",
        "pilar",
        "Puente Curvatura-Entropía su(3)/retículos y tensión Creutz Wilson (Paper Y + Paper Z, Lean 4.36.0, 0 sorry).",
        "vault/VERDAD_OASIS.md",
    )
    add_node(
        "c99_evolution",
        "benchmark",
        "L=2^4: K_eff -0.409235 -> +0.405826 (t=10); L=3^4: K_eff -0.382315 -> +0.413178 (t=10, <P>=0.47873).",
        "tools/oasis_evolution_operator.c",
    )

    if "paper_y_orbit_curvature_entropy_bound" in nodes and "PaperY_Entropy_Curvature_Margin" in nodes:
        add_edge("paper_y_orbit_curvature_entropy_bound", "verified_by", "PaperY_Entropy_Curvature_Margin")
        add_edge("pilar_389", "anchored_in", "paper_y_orbit_curvature_entropy_bound")
    if "paper_z_sovereign_synthesis" in nodes and "PaperZ_Sovereign_Synthesis" in nodes:
        add_edge("paper_z_sovereign_synthesis", "verified_by", "PaperZ_Sovereign_Synthesis")
        add_edge("paper_z_sovereign_synthesis", "extends", "paper_y_orbit_curvature_entropy_bound")
        add_edge("paper_z_sovereign_synthesis", "evidenced_by", "c99_evolution")

    # 3. Nodos del Diccionario Soberano (sovereign_catalog)
    for mod in sorted(ROOT.glob("sovereign_catalog/*.py")):
        add_node(mod.stem, "module", f"Módulo soberano {mod.name}", str(mod))

    graph = {"nodes": nodes, "edges": edges}
    GRAPH_OUT.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_OUT.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return graph

def query_graph(q: str) -> str:
    t0 = time.perf_counter()
    graph = json.loads(GRAPH_OUT.read_text(encoding="utf-8")) if GRAPH_OUT.exists() else build_graph()
    terms = set(re.findall(r"[a-z0-9_áéíóúñ]+", q.lower()))
    hits = []
    for nid, node in graph["nodes"].items():
        blob = f"{nid} {node['type']} {node['summary']}".lower()
        score = sum(1 for t in terms if t in blob)
        if score > 0:
            hits.append((score, node))
    hits.sort(key=lambda x: x[0], reverse=True)

    lines = []
    selected_ids = set()
    for _, node in hits[:4]:
        selected_ids.add(node["id"])
        lines.append(f"[{node['type'].upper()}] {node['id']}: {node['summary']} ({node['ref']})")

    for e in graph["edges"]:
        if e["from"] in selected_ids or e["to"] in selected_ids:
            lines.append(f"  -> {e['from']} --({e['rel']})--> {e['to']}")

    dt_ms = (time.perf_counter() - t0) * 1000.0
    header = f"=== GRAPHITY ({len(graph['nodes'])} nodos, {len(graph['edges'])} aristas | {dt_ms:.2f} ms) ==="
    return header + "\n" + ("\n".join(lines) if lines else "Sin nodos coincidentes.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        g = build_graph()
        print(f"✅ Grafo Graphity compilado: {len(g['nodes'])} nodos, {len(g['edges'])} aristas.")
    else:
        q = " ".join(sys.argv[1:]).strip() or "paper_z pilar_389 c99_evolution"
        print(query_graph(q))
