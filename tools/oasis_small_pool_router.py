import json
import sys
import time
import urllib.request
from oasis_golden_rag import retrieve_fast

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODELS = {
    "0.5b": "oasis-flash:0.5b",
    "1.5b": "oasis-crm:1.5b",
}

def query_pool(question: str, tier: str = "0.5b") -> None:
    t0 = time.perf_counter()
    context = retrieve_fast(question)
    t_rag = time.perf_counter() - t0

    print(f"=== RAG FUENTES PREFERIDAS ({t_rag:.3f}s) ===")
    print(context)

    if tier == "extract":
        return

    model_name = MODELS.get(tier, MODELS["0.5b"])
    prompt = (
        f"CONTEXTO VERIFICADO:\n{context}\n\n"
        f"PREGUNTA: {question}\n"
        "Responde en español en máximo 3 puntos breves copiando las cifras exactas del contexto y respetando los límites de alcance:"
    )
    payload = json.dumps({
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "24h",
        "options": {
            "num_thread": 2,
            "num_ctx": 1024,
            "num_predict": 140,
            "temperature": 0.05,
        },
    }).encode("utf-8")

    req = urllib.request.Request(OLLAMA_API, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    t_tot = time.perf_counter() - t0
    print(f"\n=== AGENTE {model_name} ({t_tot:.2f}s total) ===")
    print(data.get("response", "").strip())

if __name__ == "__main__":
    tier = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("extract", "0.5b", "1.5b") else "0.5b"
    q_args = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] in ("extract", "0.5b", "1.5b") else sys.argv[1:]
    q = " ".join(q_args).strip() or "Valores exactos de K_int y K_proj del Paper Y en su(3), L=2^4 y L=3^4"
    query_pool(q, tier)
