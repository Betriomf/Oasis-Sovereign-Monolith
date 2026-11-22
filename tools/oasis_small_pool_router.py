import json
import sys
import time
import urllib.request
from oasis_graphity_index import query_graph
from oasis_golden_rag import retrieve_fast

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODELS = {"0.5b": "oasis-flash:0.5b", "1.5b": "oasis-crm:1.5b"}

def query_pool(question: str, tier: str = "graph") -> None:
    t0 = time.perf_counter()
    graph_ctx = query_graph(question)
    rag_ctx = retrieve_fast(question)
    t_local = (time.perf_counter() - t0) * 1000.0

    print(graph_ctx)
    print(f"\n=== RAG FUENTES PREFERIDAS ({t_local:.2f} ms total) ===")
    print(rag_ctx)

    if tier in ("graph", "extract"):
        return

    model_name = MODELS.get(tier, MODELS["0.5b"])
    prompt = f"CONTEXTO:\n{graph_ctx}\n{rag_ctx}\nPREGUNTA: {question}\nResponde en 2 líneas exactas:"
    payload = json.dumps({
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "24h",
        "options": {"num_thread": 2, "num_ctx": 1024, "num_predict": 100, "temperature": 0.05},
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_API, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    print(f"\n=== AGENTE {model_name} ===")
    print(data.get("response", "").strip())

if __name__ == "__main__":
    modes = ("graph", "extract", "0.5b", "1.5b")
    tier = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in modes else "graph"
    q_args = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] in modes else sys.argv[1:]
    q = " ".join(q_args).strip() or "paper_y paper_z pilar_389 bitcoin_ots_seal"
    query_pool(q, tier)
